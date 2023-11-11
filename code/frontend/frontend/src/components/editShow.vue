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
      <form @submit.prevent="editShow" class="container mt-5">
        <fieldset>
          <legend>Edit Show ID: {{ this.$route.params.showId }}</legend>
          <p class="text-primary">
            Capacity: {{ this.$route.params.capacity }}
          </p>
          <p class="text-primary">Venue ID: {{ this.$route.params.id }}</p>
          <div class="form-group">
            <label for="name">Show Name</label>
            <input
              type="text"
              id="name"
              v-model="show.name"
              :placeholder="this.$route.params.name"
              class="form-control"
            />
          </div>
          <div class="form-group">
            <label for="rating">Rating</label>
            <input
              type="number"
              id="rating"
              v-model="show.rating"
              :placeholder="this.$route.params.rating"
              class="form-control"
              step="any"
            />
          </div>
          <div class="form-group">
            <label for="tags">Tags</label>
            <input
              type="text"
              id="tags"
              v-model="show.tags"
              :placeholder="this.$route.params.tags"
              class="form-control"
            />
          </div>
          <div class="form-group d-flex">
            <div class="flex-fill">
              <label for="start">Start</label>
              <input
                type="datetime-local"
                id="start"
                v-model="show.start"
                :placeholder="
                  formatDateTimePlaceholder(this.$route.params.start)
                "
                class="form-control"
              />
            </div>

            <div class="flex-fill">
              <label for="end">End</label>
              <input
                type="datetime-local"
                id="end"
                v-model="show.end"
                :placeholder="formatDateTimePlaceholder(this.$route.params.end)"
                class="form-control"
              />
            </div>
          </div>
          <div class="form-group">
            <label for="price">Price</label>
            <input
              type="number"
              id="price"
              v-model="show.price"
              class="form-control"
            />
          </div>
          <button type="submit" class="btn btn-primary">Edit</button>
        </fieldset>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "editShow",
  data() {
    return {
      show: {
        name: this.$route.params.name,
        rating: this.$route.params.rating,
        tags: this.$route.params.tags,
        capacity: this.$route.params.capacity,
        venue_id: this.$route.params.id,
        price: this.$route.params.price,
        start: this.$route.params.start,
        end: this.$route.params.end,
        showId: this.$route.params.showId,
        left: this.$route.params.left,
        timestamp: this.$route.params.timestamp,
      },
    };
  },
  methods: {
    editShow() {
      this.show.start = new Date(this.show.start);
      this.show.end = new Date(this.show.end);
      const jwtToken = localStorage.getItem("access_token");
      axios
        .post("http://localhost:5000/editShow", this.show, {
          headers: {
            Authorization: `Bearer ${jwtToken}`,
          },
        })
        .then((response) => {
          console.log(response);
          this.$router.push("/admindashboard");
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
    formatDateTimePlaceholder(dateTime) {
      const dateObj = new Date(dateTime.replace(" ", "T"));
      const year = dateObj.getUTCFullYear();
      const month = String(dateObj.getUTCMonth() + 1).padStart(2, "0");
      const day = String(dateObj.getUTCDate()).padStart(2, "0");
      const hours = String(dateObj.getUTCHours()).padStart(2, "0");
      const minutes = String(dateObj.getUTCMinutes()).padStart(2, "0");
      return `${year}-${month}-${day}T${hours}:${minutes}`;
    },
  },
};
</script>
