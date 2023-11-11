<template>
  <!-- eslint-disable vue/no-use-v-if-with-v-for,vue/no-confusing-v-for-v-if -->
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
        <div v-if="errorMessage === ''">
          <div class="collapse navbar-collapse" id="navbarColor01">
            <ul class="navbar-nav me-auto">
              <li class="nav-item">
                <a
                  class="nav-link active text-white"
                  href="http://localhost:8080/addVenue"
                  >Add Venue
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
    <div>
      <div v-if="errorMessage === ''">
        <div
          v-if="venues.length === 0 && shows.length === 0"
          class="alert alert-info mt-3"
        >
          No shows or venues created
        </div>
        <div v-else>
          <div class="container">
            <div
              v-for="venue in venues"
              :key="venue.venue_id"
              class="card my-3"
            >
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-center">
                  <h2 class="card-title">{{ venue.name }}</h2>
                  <div>
                    <button
                      type="button"
                      class="btn btn-outline-dark mx-1"
                      @click="editVenue(venue)"
                    >
                      Edit Venue
                    </button>
                    <button
                      type="button"
                      class="btn btn-outline-dark mx-1"
                      @click="confirmDeleteVenue(venue)"
                    >
                      Delete Venue
                    </button>
                    <button
                      type="button"
                      class="btn btn-outline-dark mx-1"
                      @click="addShow(venue)"
                    >
                      Add Show
                    </button>
                    <button
                      type="button"
                      class="btn btn-outline-dark mx-1"
                      @click="generateAndDownloadCSV(venue)"
                    >
                      Export as CSV
                    </button>
                  </div>
                </div>
                <p class="card-text">{{ venue.place }}</p>
                <p class="card-text">Capacity: {{ venue.capacity }}</p>
                <div class="row">
                  <div
                    v-for="show in shows"
                    :key="show.show_id"
                    v-if="show.venue_id === venue.venue_id"
                    class="col-sm-4 my-3"
                  >
                    <div class="card" style="max-width: 15rem">
                      <div class="card-body">
                        <p class="card-title">{{ show.name }}</p>
                        <p class="card-text">Start: {{ show.start }}</p>
                        <p class="card-text">End: {{ show.end }}</p>
                        <div>
                          <button
                            type="button"
                            class="btn btn-outline-dark mr-2"
                            @click="editShow(show, venue)"
                          >
                            Edit
                          </button>
                          <button
                            type="button"
                            class="btn btn-outline-dark"
                            @click="confirmDeleteShow(show)"
                          >
                            Delete
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else-if="errorMessage !== ''">
        <div class="alert alert-danger mt-3">
          Admin access required. Please log in as an admin. {{ errorMessage }}
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
  name: "adminDashboard",
  data() {
    return {
      venues: [],
      shows: [],
      errorMessage: "",
    };
  },
  methods: {
    confirmDeleteVenue(venue) {
      if (
        window.confirm(
          "Please confirm: Deleting this Venue will also remove any associated bookings and shows. Are you sure you want to proceed?"
        )
      ) {
        this.deleteVenueAndShows(venue);
      }
    },
    confirmDeleteShow(show) {
      if (
        window.confirm(
          "Please confirm: Deleting this show will also remove any bookings associated with this show. Are you sure you want to proceed?"
        )
      ) {
        this.deleteShow(show);
      }
    },
    admindash() {
      const path = "http://localhost:5000/admindashboard";
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
            this.venues = res.data.venues;
            this.shows = res.data.shows;
          } else {
            this.errorMessage = "Authorization required";
          }
        })
        .catch((err) => {
          this.errorMessage = "Authorization required";
          console.error(err);
        });
    },
    editVenue(venue) {
      this.$router.push({
        name: "editVenue",
        params: {
          id: venue.venue_id,
          name: venue.name,
          place: venue.place,
          capacity: venue.capacity,
        },
      });
    },
    addShow(venue) {
      this.$router.push({
        name: "addShow",
        params: {
          id: venue.venue_id,
          capacity: venue.capacity,
        },
      });
    },
    editShow(show, venue) {
      this.$router.push({
        name: "editShow",
        params: {
          id: venue.venue_id,
          capacity: venue.capacity,
          name: show.name,
          rating: show.rating,
          tags: show.tags,
          price: show.price,
          start: show.start,
          end: show.end,
          showId: show.show_id,
          timestamp: show.timestamp,
          left: show.left,
        },
      });
    },
    deleteShow(show) {
      const jwtToken = localStorage.getItem("access_token");
      axios
        .delete(`http://localhost:5000/deleteShow/${show.show_id}`, {
          headers: {
            Authorization: `Bearer ${jwtToken}`,
          },
        })
        .then((response) => {
          console.log(response.data);

          this.shows = this.shows.filter((s) => s.show_id !== show.show_id);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    deleteVenueAndShows(venue) {
      const jwtToken = localStorage.getItem("access_token");
      axios
        .delete(`http://localhost:5000/deleteVenue/${venue.venue_id}`, {
          headers: {
            Authorization: `Bearer ${jwtToken}`,
          },
        })
        .then((response) => {
          console.log(response.data);
          this.venues = this.venues.filter(
            (v) => v.venue_id !== venue.venue_id
          );
        })
        .catch((error) => {
          console.error(error);
        });
    },
    generateAndDownloadCSV(venue) {
      axios
        .post("http://localhost:5000/generate-csv", {
          venue_id: venue.venue_id,
        })
        .then((response) => {
          console.log("Generate CSV Response:", response.data);
          this.pollForCSV();
        })
        .catch((error) => {
          console.error("Error generating CSV:", error);
        });
    },

    pollForCSV() {
      const intervalId = setInterval(() => {
        axios
          .get("http://localhost:5000/check-csv")
          .then((response) => {
            console.log("CSV Check Response:", response.data);
            if (response.data.exists) {
              clearInterval(intervalId);
              console.log("CSV File Detected. Initiating Download...");
              this.downloadCSV();
            }
          })
          .catch((error) => {
            console.error("Error checking CSV:", error);
          });
      }, 2000); // Poll every 2 seconds
    },

    downloadCSV() {
      window.open("http://localhost:5000/download-csv");
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

  created() {
    this.admindash();
  },
};
</script>
