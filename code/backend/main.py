from flask import Flask, jsonify, request, redirect, send_file
from jinja2 import Template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from datetime import datetime,timedelta
from pytz import timezone
from dateutil import parser
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
import os
from celery import Celery
import smtplib
from celery.schedules import crontab
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime, timedelta
from flask_caching import Cache
from time import perf_counter_ns

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r"/*":{'origins':"*"}})


app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///showspotdb.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379'
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] ="localhost"
app.config['CACHE_REDIS_PORT'] = 6379
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'super-secret' 
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authorization'
app.config['SECURITY_TOKEN_AUTHENTICATION_KEY'] = 'auth_token'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
cache = Cache(app)


class User(db.Model):
  __tablename__ = 'User'
  ID = db.Column(db.Integer ,primary_key =True, unique = False, nullable = True, autoincrement=True)
  username = db.Column(db.String ,unique = False, nullable = True )
  email = db.Column(db.String,  unique = True, nullable = True )
  password =db.Column(db.String, unique = False, nullable = False )
  active = db.Column(db.Integer,  unique = False, nullable = False )
  role_name=db.Column(db.String, nullable=False, unique = False)
  last_visited=db.Column(db.String, nullable=False, unique = False)
  
  bookings = db.relationship('Booking', back_populates='user')

class venue(db.Model):
  __tablename__ = 'venue'
  venue_id = db.Column(db.Integer , primary_key =True, nullable = True, autoincrement=True, unique = True)
  capacity = db.Column(db.Integer ,unique = False, nullable = False )
  name = db.Column(db.String, unique = False, nullable = False )
  place = db.Column(db.String ,unique = False, nullable = False )

  shows = db.relationship('Show', back_populates='venue')
  booking = db.relationship('Booking', back_populates='venue')
  

class Show(db.Model):
    __tablename__ = 'Show'
    show_id = db.Column(db.Integer, primary_key=True,nullable=True, autoincrement=True, unique = False)
    name = db.Column(db.String, nullable=False, unique = False)
    rating = db.Column(db.Float, nullable=False, unique = False)
    tags = db.Column(db.String, nullable=False, unique = False)
    start = db.Column(db.String, nullable=False, unique = False)
    end = db.Column(db.String, nullable=False, unique = False)
    capacity = db.Column(db.Integer, nullable=False, unique = False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.venue_id'), nullable=False, unique = False)
    price = db.Column(db.Float, nullable=False, unique = False)
    timestamp = db.Column(db.String, nullable=False, unique = False)
    left=db.Column(db.Integer, nullable=False, unique = False)
    
    venue = db.relationship('venue', back_populates='shows')
    bookings = db.relationship('Booking', back_populates='show')


class Booking(db.Model):
    __tablename__ = 'Booking'
    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    show_id = db.Column(db.Integer, db.ForeignKey('Show.show_id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.venue_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.ID'), nullable=False)
    num_tickets = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.String, nullable=False, unique = False)
    
    user = db.relationship('User', back_populates='bookings')
    venue = db.relationship('venue', back_populates='booking')
    show = db.relationship('Show', back_populates='bookings')

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['result_backend'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'],enable_utc=False,timezone='Asia/Kolkata')
celery.conf.update(app.config)
celery.conf.broker_connection_retry_on_startup = True


@celery.task
def generate_csv_task(csv_data):
    csv_file_path = 'static/data.csv'
    with open(csv_file_path, 'w') as f:
        f.write(csv_data)

@app.route('/generate-csv', methods=['POST'])
def generate_csv():
    venue_id = request.json.get('venue_id')
    shows_list = Show.query.filter_by(venue_id=venue_id).all()
    csv_data = 'Show Name, Seats Booked, Rating\n'
    for shows in shows_list:
        csv_data += f"{shows.name}, {shows.capacity - shows.left}, {shows.rating}\n"
    generate_csv_task.apply_async(args=(csv_data,)) 
    return {'message': 'CSV generation task started'}, 200


@app.route('/check-csv')
def check_csv():
    csv_exists = os.path.exists('static/data.csv')
    return {'exists': csv_exists}, 200

@app.route('/download-csv')
def download_csv():
    csv_file_path = 'static/data.csv'
    return send_file(csv_file_path, as_attachment=True)

celery.conf.beat_schedule = {
    'send-email-task': {
        'task': 'main.send_email_task',  
        'schedule': crontab(hour=17, minute=30),
    },

    'send-monthly-report': {
        'task': 'main.send_monthly_report',
        'schedule': crontab(day_of_month=1, hour=0, minute=0), #day_of_month=1, hour=0, minute=0
        },
}

@celery.task
def send_monthly_report():
    with app.app_context(): 
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'fnathaniaf16@gmail.com' 
        smtp_password = 'wwzhquyhwcjbafbv' 
        role = 'user' 
        users = User.query.filter_by(role_name=role).all()
        current_date = datetime.now()
        year = current_date.year 
        month = current_date.month 

        for user in users:
            bookings = Booking.query.filter_by(user_id=user.ID).all()
            msg = MIMEMultipart()
            msg['From'] = smtp_username
            msg['To'] = user.email
            msg['Subject'] = "SaveASeat: Monthly Report"
            
            if bookings:
                message = "Hello {},\n\nWe have attached the monthly report for your review.\n\nBest regards,\nSaveASeat".format(user.username)
                text_part = MIMEText(message, 'plain')
                msg.attach(text_part)

                report_html = generate_monthly_report(year, month,user.ID)
                
                report_part = MIMEApplication(report_html, Name="monthly_report.html")
                report_part['Content-Disposition'] = f'attachment; filename="monthly_report.html"'
                msg.attach(report_part)
            else:
                message = "Hello {},\n\nYou have not booked any shows in the past month.\n\nBest regards,\nSaveASeat".format(user.username)
                text_part = MIMEText(message, 'plain')
                msg.attach(text_part)  

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(smtp_username, user.email, msg.as_string())
        

def generate_monthly_report(year, month,user_id):
    bookings = Booking.query.filter(user_id == user_id).all()
    user_stats = []
    for booking in bookings:
        user_stats.append({
            'show_name': booking.show.name,
            'venue_name': booking.venue.name,
            'location': booking.venue.place,
            'rating': booking.show.rating,
            'booked_seats': booking.num_tickets,
        })
    template = Template(open('report_template.html').read())
    report_html = template.render(user_stats=user_stats, month_year=f'{month}/{year}')
    return report_html

@celery.task
def send_email_task():
    with app.app_context():
        threshold_time = datetime.utcnow() - timedelta(hours=24)
        threshold_time_str = threshold_time.strftime('%d-%m-%Y %H:%M:%S.%f')
        inactive_users = User.query.filter(User.last_visited > threshold_time_str).all()
        
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'fnathaniaf16@gmail.com' 
        smtp_password = 'wwzhquyhwcjbafbv'

        for user_instance in inactive_users:
            msg = MIMEMultipart()
            msg['From'] = smtp_username
            msg['To'] = user_instance.email
            msg['Subject'] = "Reminder: Visit our site!"
            message = "Hello {},\n\nWe noticed that you haven't visited our site in the past 24 hours. We invite you to explore our latest updates.\n\nBest regards,\nSaveASeat".format(user_instance.username)  # Update the message content

            msg.attach(MIMEText(message))

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(smtp_username, user_instance.email, msg.as_string())

            
@app.route('/', methods=['GET'])
def login():
    return("Hello, world!")

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    existing_user = User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'This username or email already exists'}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    time=datetime.now(timezone("Asia/Kolkata")).strftime('%d-%m-%Y %H:%M:%S.%f')
    new_user = User(username=username, email=email, password=hashed_password, active=1, role_name='user',last_visited=time)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login/user', methods=['POST'])
def login_user():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'Invalid username or email'}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid password'}), 401
    if user:
        user.last_visited = datetime.now(timezone("Asia/Kolkata")).strftime('%d-%m-%Y %H:%M:%S.%f')
        db.session.commit()
        access_token = create_access_token(identity=user.ID)
        return jsonify({'access_token':access_token,'message':"User login successful"}),200


@app.route('/login/admin', methods=['POST'])
def loginAdmin():
    data = request.get_json()

    admin_id = data.get('id')
    username = data.get('username')
    password = data.get('password')

    admin = User.query.filter_by(ID=admin_id, role_name='admin',username=username).first()

    if not admin:
        return jsonify({'message': 'Invalid credentials'}), 404

    if not bcrypt.check_password_hash(admin.password, password):
        return jsonify({'message': 'Incorrect password'}), 404
    if admin:
        admin.last_visited = datetime.now(timezone("Asia/Kolkata")).strftime('%d-%m-%Y %H:%M:%S.%f')
        db.session.commit()
        access_token = create_access_token(identity=admin.ID)
        return jsonify({'access_token':access_token,'message':"Admin login successful"}),200



def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        print(current_user)
        user_obj = User.query.get(current_user)
        if user_obj.role_name != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

def user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        user_obj = User.query.get(current_user) 
        if user_obj.role_name != 'user':
            return jsonify({'message': 'User access required'}), 403
        return fn(*args, **kwargs)
    return wrapper


@app.route('/admindashboard', methods=['GET'])
@jwt_required()
@admin_required
def admindash():
    venues = venue.query.all()
    venues_list = [{
        'venue_id': venue.venue_id,
        'capacity': venue.capacity,
        'name': venue.name,
        'place': venue.place
    } for venue in venues]
    shows = Show.query.all()
    shows_list = [{'show_id': show.show_id,
        'name': show.name,
        'start': show.start,
        'end': show.end,
        'venue_id':show.venue_id,
        'id': show.venue_id,
        'capacity': show.capacity,
        'timestamp':show.timestamp,
        'rating': show.rating,
        'tags': show.tags,
        'price': show.price,
        'left':show.left
    } for show in shows]
    return jsonify({'venues': venues_list, 'shows': shows_list})


@app.route('/addVenue', methods=['GET','POST'])
@jwt_required()
@admin_required
def addVenue():
    if request.method == "POST":
        post_data = request.get_json()
        theater = post_data['name']
        location = post_data['place']
        persons= post_data['capacity']

        a = venue(name=theater, place=location, capacity=persons)
        db.session.add(a)
        db.session.commit()

        return redirect('/admindashboard')
    else:
        return {"error": "Venue not found"}, 404

@app.route('/addShow', methods=['GET','POST'])
@jwt_required()
@admin_required
def addShow():
    if request.method == "POST":
        post_data = request.get_json()
        show_name = post_data['name']
        show_rating = post_data['rating']
        show_tags = post_data['tags']
        show_start = datetime.fromisoformat(post_data['start'].replace("Z", "+00:00"))
        show_end = datetime.fromisoformat(post_data['end'].replace("Z", "+00:00"))
        show_capacity = post_data['capacity']
        show_venue_id = post_data['venue_id']
        show_price = post_data['price']
        show_left= post_data['capacity']
        time=datetime.now(timezone("Asia/Kolkata")).strftime('%d-%m-%Y %H:%M:%S.%f')

        new_show = Show(name=show_name, rating=show_rating, tags=show_tags, start=show_start, end=show_end, capacity=show_capacity, venue_id=show_venue_id, price=show_price,timestamp=time,left=show_left)
        db.session.add(new_show)
        db.session.commit()

        return redirect('/admindashboard')
    else:
        return {"error": "Show not found"}, 404
    
@app.route('/editVenue', methods=['GET','POST'])
@jwt_required()
@admin_required
def editVenue():
    data = request.get_json()
    Venue = venue.query.get(data['id'])
    if Venue:
        Venue.name = data['name']
        Venue.place = data['place']
        Venue.capacity = data['capacity']
        db.session.commit()
        return redirect('/admindashboard')
    else:
        return {"error": "Venue not found"}, 404
    
@app.route('/editShow', methods=['GET','POST'])
@jwt_required()
@admin_required
def editShow():
    data = request.get_json()
    show = Show.query.get(data['showId'])
    if show:
        show.name = data['name']
        show.rating = data['rating']
        show.tags = data['tags']
        show.start = datetime.fromisoformat(data['start'].replace("Z", "+00:00"))
        show.end = datetime.fromisoformat(data['end'].replace("Z", "+00:00"))
        show.capacity = data['capacity']
        show.venue_id = data['venue_id']
        show.price = data['price']
        show.timestamp = data['timestamp']
        show.left = data['left']
        show.show_id = data['showId']
        db.session.commit()
        return redirect('/admindashboard')
    else:
        return {"error": "Show not found"}, 404
    
@app.route('/deleteShow/<int:show_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_show(show_id):
    show_to_delete = Show.query.get(show_id)
    
    if show_to_delete:

        bookings_to_delete = Booking.query.filter_by(show_id=show_id).all()
        for booking in bookings_to_delete:
            db.session.delete(booking)
        
        db.session.delete(show_to_delete)
        db.session.commit()
        return jsonify(message='Show deleted successfully'), 200
    else:
        return jsonify(error='Show not found'), 404

@app.route('/deleteVenue/<int:venue_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_venue_and_shows(venue_id):
    venue_to_delete = venue.query.get(venue_id)
    if venue_to_delete:

        booking_to_delete= Booking.query.filter_by(venue_id=venue_id).all()
        for bookings_to_delete in booking_to_delete:
            db.session.delete(bookings_to_delete)

        shows_to_delete = Show.query.filter_by(venue_id=venue_id).all()
        for show_to_delete in shows_to_delete:
            db.session.delete(show_to_delete)
        
        db.session.delete(venue_to_delete)
        db.session.commit()
        return jsonify({'message': 'Venue and associated shows deleted successfully.'}), 200
    else:
        return jsonify({'error': 'Venue not found.'}), 404

@app.route('/explore', methods=['GET'])
@jwt_required()
@user_required
@cache.cached(timeout=300) #5min
def get_shows():
    print("Response served from cache")
    now = datetime.now(timezone("Asia/Kolkata"))
    start = perf_counter_ns()
    venues = venue.query.all()
    hi =get_jwt_identity()
    print(hi)
    venues_list = [{
        'venue_id': venue.venue_id,
        'capacity': venue.capacity,
        'name': venue.name,
        'place': venue.place
    } for venue in venues]
    shows = Show.query.all()
    stop = perf_counter_ns()
    print("Time Taken:" , stop - start)
    shows_list = [{'show_id': show.show_id,
        'name': show.name,
        'start': show.start,
        'end': show.end,
        'venue_id':show.venue_id,
        'id': show.venue_id,
        'capacity': show.capacity,
        'timestamp':show.timestamp,
        'rating': show.rating,
        'tags': show.tags,
        'price': show.price,
        'left':show.left
    } for show in shows if parser.parse(show.start) > now]

    return jsonify({'venues': venues_list, 'shows': shows_list})

@app.route('/BookShow', methods=['POST'])
@jwt_required()
@user_required
def booking():
    if request.method == "POST":
        post_data = request.get_json()
        venue = post_data['venue_id']
        show = post_data['show_id']
        user= get_jwt_identity()
        ticket= post_data['tickets']
        remaining= post_data['left']
        timestamp=datetime.now(timezone("Asia/Kolkata")).strftime('%d-%m-%Y %H:%M:%S.%f')
        a = Booking(venue_id=int(venue), show_id=show, user_id=user, num_tickets=int(ticket),timestamp=timestamp)
        db.session.add(a)
        b = Show.query.get(show)
        if b:
            b.left = int(remaining) - int(ticket)
            db.session.commit()
        return redirect('/explore')
    else:
        return {"error": "Venue not found"}, 404

@app.route('/bookings', methods=['GET'])
@jwt_required()
@user_required
def bookings():
    user_id = get_jwt_identity()
    user_bookings = Booking.query.filter_by(user_id=user_id).all()
    booking_list = []

    for booking in user_bookings:
        show = Show.query.get(booking.show_id)
        booking_info = {
            'show_name': show.name,
            'start_time': show.start,
            'end_time': show.end,
            'num_tickets': booking.num_tickets  
        }
        booking_list.append(booking_info)

    return jsonify({'bookings': booking_list}), 200


@app.route('/clear-cache', methods=['POST'])
def clear_cache():
    try:
        cache.clear()
        return jsonify({"message": "Cache cleared successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
