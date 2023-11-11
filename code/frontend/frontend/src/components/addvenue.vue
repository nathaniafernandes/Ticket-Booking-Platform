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
        <a
          class="navbar-brand text-white"
          href="http://localhost:8080/admindashboard"
          >Save A Seat</a
        >
        <div>
          <div class="collapse navbar-collapse" id="navbarColor01">
            <ul class="navbar-nav me-auto">
              <li class="nav-item">
                <a
                  class="nav-link active text-white"
                  href="http://localhost:8080/adminDashboard"
                  >Dashboard
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
    <div class="col-6 mx-auto">
      <form @submit.prevent="addVenue" class="container mt-5">
        <fieldset>
          <legend>Add Venue</legend>
          <div class="form-group">
            <label for="name">Name</label>
            <input
              type="text"
              id="name"
              v-model="venue.name"
              class="form-control"
            />
          </div>
          <div class="form-group">
            <label for="place">Place</label>
            <input
              type="text"
              id="place"
              v-model="venue.place"
              class="form-control"
            />
          </div>
          <div class="form-group">
            <label for="capacity">Capacity</label>
            <input
              type="number"
              id="capacity"
              v-model="venue.capacity"
              class="form-control"
            />
          </div>
          <button type="submit" class="btn btn-primary">Add Venue</button>
        </fieldset>
      </form>
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
  name: "addVenue",
  data() {
    return {
      msg: "",
      venue: {
        name: "",
        place: "",
        capacity: 0,
      },
    };
  },
  methods: {
    addVenue() {
      const jwtToken = localStorage.getItem("access_token");
      axios
        .post("http://localhost:5000/addVenue", this.venue, {
          headers: {
            Authorization: `Bearer ${jwtToken}`,
          },
        })
        .then((response) => {
          console.log(response);
          this.$router.push("/admindashboard");
        })
        .catch((error) => {
          console.error(error);
        });
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
};
</script>
