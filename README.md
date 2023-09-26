# SaveASeat- Ticket Booking Platform

## Table of Contents
- [Description](#description)
- [Technologies Used](#technologies-used)
- [Directory Structure](#directory-structure)
- [Backend](#backend)
- [Frontend](#frontend)
- [Installation](#installation)
- [Usage](#usage)
- [Celery & Redis](#celery--redis)

## Description
This project is a multi-user ticket booking platform for booking show tickets for various movies. It includes features such as user signup and login, admin management, theatre and show management, booking show tickets, search for shows/theatres, backend jobs for export, reporting, and alerts, as well as caching for performance enhancement.

## Technologies Used
- Flask for API
- VueJS for UI
- SQLite for database
- Redis for caching
- Celery for batch jobs

## Directory Structure

```
21f1000454/
├── Project Report.pdf
├── code/
| ├── backend/
| | ├── Pipfile
| | ├── Pipfile.lock
| | ├── main.py
| | ├── report_template.html
| | ├── requirements.txt
| | ├── static/
| | | └──data.csv
| | ├──instance/
| | | └──showspotdb.sqlite3
| | ├──pycache/
| | | ├──celery_worker.cpython-310.pyc
| | | ├──database.cpython-310.pyc
| | | ├──mail.cpython-310.pyc
| | | ├──main.cpython-310.pyc
| | | ├──models.cpython-310.pyc
| | | └──tasks.cpython-310.pyc
| | ├──celerybeat-schedule
| | └──dump.rdb
| └──frontend/
| | ├──frontend/
| | | ├──public/
| | | | ├──SAS-3.jpeg
| | | | ├──favicon.ico
| | | | └──index.html
| | | └──src/
| | | | ├──App.vue
| | | | ├──assets/
| | | | | ├──SAS-3.jpeg
| | | | | └──logo.png
| | | | ├──components/
| | | | | └── ...
| | | | ├──main.js
| | | | └──router/
| | | | | └──index.js
| | ├── babel.config.js
| | ├── jsconfig.json
| | ├── package-lock.json
| | ├── package.json
| | └──vue.config.js
└── code/README.md

```

## Backend
The backend of the project is built using Flask, and it includes user and admin functionalities, theatre and show management, booking show tickets, and more. It also integrates Celery for handling batch jobs and Redis for caching. The SQLite database is used for data storage.

## Frontend
The frontend is developed using VueJS and includes components for user interface elements such as user registration, login, booking shows, managing theatres and shows, and more.

## Installation
1. Clone this repository.
2. Set up the backend environment using the provided `Pipfile` and `Pipfile.lock` files.
3. Set up the virtual environment using `pipenv shell`.
4. Install the required dependencies using `pipenv install -r requirements.txt`.
5. Set up the frontend environment using the provided `package.json` and `package-lock.json` files.
6. Install the required dependencies using `npm install` within the `frontend` directory.
7. Install the required dependencies using `npm install` within the `frontend/frontend` directory.

## Usage
1. Start the Flask backend server by running `pipenv run python main.py` within the `backend` directory.
2. Start the VueJS frontend server by running `npm run serve` within the `frontend/frontend` directory.
3. Access the application in your web browser at `http://localhost:8080`.

## Celery & Redis 
(Run all of the below in WSL terminal's after creating a virtual environment using `python3 -m venv .env`, activating the virtual environment using `source .env/bin/activate` & Installing the required dependencies using `pip install -r requirements.txt`)
1. To start redis run `redis-server`.
2. Make necessary changes to "smtp_username" & "smtp_password" in the main.py file to run both the celery tasks.
3. `celery -A main.celery worker` - for monthly reports.
4. `celery -A main.celery worker -l info` - to run generate CSV task and for daily reminders.
5. `celery -A main.celery beat --loglevel=info` - for schedule the tasks.
6. To stop redis `sudo service redis-server stop`.
