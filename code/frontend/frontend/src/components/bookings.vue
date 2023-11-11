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
    <div class="container mt-4">
      <h2>Seats saved</h2>
      <div v-for="(booking, index) in bookings" :key="index" class="card mb-3">
        <div class="card-body">
          <h5 class="card-title">{{ booking.show_name }}</h5>
          <p class="card-text">Start Time: {{ booking.start_time }}</p>
          <p class="card-text">End Time: {{ booking.end_time }}</p>
          <p class="card-text">
            <span class="badge bg-secondary rounded-pill"
              >Tickets booked: {{ booking.num_tickets }}</span
            >
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
<style>
.nav-link {
  cursor: pointer;
}
</style>
<script>
import axios from "axios";

export default {
  name: "UserBookings",
  data() {
    return {
      bookings: [],
    };
  },
  mounted() {
    this.fetchBookings();
  },
  methods: {
    fetchBookings() {
      const path = "http://localhost:5000/bookings";
      const jwtToken = localStorage.getItem("access_token");
      axios
        .get(path, {
          headers: {
            Authorization: `Bearer ${jwtToken}`,
          },
        })
        .then((res) => {
          console.log("Server response:", res.data);
          if (res.data) {
            this.bookings = res.data.bookings;
          } else {
            this.errorMessage = "Authorization required";
          }
        })
        .catch((err) => {
          this.errorMessage = "Authorization required";
          console.error(err);
        });
    },
    confirmLogout() {
      if (confirm("Are you sure you want to logout?")) {
        this.logout();
      }
    },

    logout() {
      // Clear the cache on the server side
      axios
        .post("http://localhost:5000/clear-cache")
        .then((response) => {
          console.log("Cache cleared on server:", response.data.message);
        })
        .catch((error) => {
          console.error("Error clearing cache on server:", error);
        });

      // Remove the access token
      localStorage.removeItem("access_token");

      // Redirect to the home page
      this.$router.push("/");
    },
  },
};
</script>
