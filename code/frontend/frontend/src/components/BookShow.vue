<template>
  <div>
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/lux/bootstrap.min.css"
      integrity="sha384-9+PGKSqjRdkeAU7Eu4nkJU8RFaH8ace8HGXnkiKMP9I9Te0GJ4/km3L1Z8tXigpG"
      crossorigin="anonymous"
    />
    <nav
      class="navbar navbar-expand-lg bg-primary text-white"
      data-bs-theme="dark"
    >
      <div class="container-fluid">
        <a class="navbar-brand text-white" href="http://localhost:8080/explore"
          >Save A Seat</a
        >
        <div>
          <div class="collapse navbar-collapse" id="navbarColor01">
            <ul class="navbar-nav me-auto">
              <li class="nav-item">
                <a
                  class="nav-link active text-white"
                  href="http://localhost:8080/explore"
                  >Explore
                </a>
              </li>
            </ul>
            <div class="collapse navbar-collapse" id="navbarColor01">
              <ul class="navbar-nav me-auto">
                <li class="nav-item">
                  <a class="nav-link active text-white" @click="confirmLogout"
                    >Logout</a
                  >
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </nav>
    <div class="container mt-5">
      <h2 class="mb-4">Save a Seat {{ this.$route.query.userId }}</h2>

      <!-- Show Details -->
      <div class="mb-4">
        <h3>
          Show: <span class="font-weight-normal">{{ show.name }}</span>
        </h3>
        <p>
          Venue: <span class="font-weight-normal">{{ venue.venue_name }}</span>
        </p>
        <p>
          Available Seats:
          <span class="font-weight-normal">{{ show.left }}</span>
        </p>
        <p>
          Price per Ticket:
          <span class="font-weight-normal">{{ show.price }}</span>
        </p>
        <p>
          Show Time:
          <span class="font-weight-normal"
            >{{ show.start }} - {{ show.end }}</span
          >
        </p>
      </div>

      <!-- Booking Form -->
      <form @submit.prevent="bookShow" class="mb-3" required>
        <div class="form-group">
          <label for="tickets">Number of Tickets:</label>
          <input
            type="number"
            id="tickets"
            v-model="show.tickets"
            min="1"
            :max="show.left"
            class="form-control"
            required
          />
        </div>

        <p>
          Total Price to be Paid:
          <span class="font-weight-bold">{{ totalPrice }}</span>
        </p>

        <button type="submit" class="btn btn-primary">Save a Seat</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "BookShow",
  data() {
    return {
      show: {
        name: this.$route.params.name, // replace with actual data
        left: this.$route.params.left,
        price: this.$route.params.price, // replace with actual data
        show_id: this.$route.params.show_id,
        start: this.$route.params.start,
        end: this.$route.params.end,
        tickets: "",
        venue_id: this.$route.params.venue_id,
      },
      venue: {
        venue_id: this.$route.params.venue_id,
        venue_name: this.$route.params.venue_name,
      },
    };
  },
  methods: {
    bookShow() {
      const jwtToken = localStorage.getItem("access_token");
      axios
        .post("http://localhost:5000/BookShow", this.show, {
          headers: {
            Authorization: `Bearer ${jwtToken}`,
          },
        })
        .then((response) => {
          console.log(response);
          this.$router.push("/explore");
        })
        .catch((error) => console.error(error));
    },
    confirmLogout() {
      if (confirm("Are you sure you want to logout?")) {
        this.logout();
      }
    },

    logout() {
      localStorage.removeItem("access_token");
      this.$router.push("/");
    },
  },
  computed: {
    totalPrice: function () {
      return this.show.tickets * this.show.price;
    },
  },
  mounted() {
    this.bookShow();
  },
};
</script>
