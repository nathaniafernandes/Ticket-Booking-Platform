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
        <a class="navbar-brand text-white" href="http://localhost:8080/explore"
          >Save A Seat</a
        >
        <div>
          <div class="collapse navbar-collapse" id="navbarColor01">
            <ul class="navbar-nav me-auto">
              <li class="nav-item">
                <a
                  class="nav-link active text-white"
                  href="http://localhost:8080/bookings"
                  >Bookings
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
      <div
        v-if="venues.length === 0 && shows.length === 0"
        class="alert alert-info mt-3"
      >
        No shows or venues avaliable
      </div>
      <div v-else>
        <div class="my-4">
          <div class="d-flex">
            <div class="mx-2" style="width: 200px">
              <div class="card-body">
                <div class="form-group">
                  <label for="venueDropdown">Filter by Location:</label>
                  <select
                    id="venueDropdown"
                    class="form-control"
                    v-model="selectedVenue"
                  >
                    <option value="">All Venues</option>
                    <option
                      v-for="place in uniqueVenuePlaces"
                      :key="place"
                      :value="place"
                    >
                      {{ place }}
                    </option>
                  </select>
                </div>

                <div class="form-group mt-3">
                  <label for="tagDropdown">Filter by Tag:</label>
                  <select
                    id="tagDropdown"
                    class="form-control"
                    v-model="selectedTag"
                  >
                    <option value="">All Tags</option>
                    <option v-for="tag in uniqueTags" :key="tag" :value="tag">
                      {{ tag }}
                    </option>
                  </select>
                </div>
              </div>
            </div>
            <div class="col my-4">
              <div class="container">
                <div
                  v-for="venue in filteredVenuesWithShows"
                  :key="venue.venue_id"
                  v-if="venue.shows.length > 0"
                  class="card my-3"
                >
                  <div class="card-body">
                    <div
                      class="d-flex justify-content-between align-items-center"
                    >
                      <h2 class="card-title">{{ venue.name }}</h2>
                      <!-- Here you can put other buttons if needed -->
                    </div>
                    <p class="card-text">{{ venue.place }}</p>
                    <div class="row">
                      <div
                        v-for="show in venue.shows"
                        :key="show.show_id"
                        class="col-sm-4 my-3"
                      >
                        <div class="card" style="max-width: 15rem">
                          <div class="card-body">
                            <p class="card-title">{{ show.name }}</p>
                            <p class="card-text">Start: {{ show.start }}</p>
                            <p class="card-text">End: {{ show.end }}</p>
                            <p class="card-text">
                              Seats Avaliable: {{ show.left }}
                            </p>

                            <button
                              v-if="show.left > 0"
                              type="button"
                              class="btn btn-outline-dark mr-2"
                              @click="bookShow(show, venue)"
                            >
                              Save A Seat
                            </button>
                            <button
                              v-else
                              type="button"
                              class="btn btn-outline-dark mr-2"
                              disabled
                            >
                              Housefull
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
  name: "UserExplore",
  data() {
    return {
      selectedVenue: "",
      selectedTag: "",
      venues: [],
      shows: [],
    };
  },
  methods: {
    get_shows() {
      const path = "http://localhost:5000/explore";
      const jwtToken = localStorage.getItem("access_token");
      axios
        .get(path, {
          headers: {
            Authorization: `Bearer ${jwtToken}`,
          },
        })
        .then((res) => {
          console.log(res.data);
          this.venues = res.data.venues;
          this.shows = res.data.shows;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    bookShow(show, venue) {
      this.$router.push({
        name: "BookShow",
        params: {
          venue_id: venue.venue_id,
          venue_name: venue.name,
          show_id: show.show_id,
          name: show.name,
          left: show.left,
          start: show.start,
          end: show.end,
          price: show.price,
        },
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
  computed: {
    uniqueTags() {
      const allTags = this.shows.flatMap((show) => show.tags.split(","));
      const uniqueTags = allTags.reduce((unique, tag) => {
        if (tag.trim()) {
          unique[tag.trim()] = true;
        }
        return unique;
      }, {});
      return Object.keys(uniqueTags);
    },
    uniqueVenuePlaces() {
      const uniquePlaces = [
        ...new Set(this.venues.map((venue) => venue.place)),
      ];
      return uniquePlaces;
    },
    venuesWithShows() {
      return this.venues.map((venue) => {
        return {
          ...venue,
          shows: this.shows.filter((show) => show.venue_id === venue.venue_id),
        };
      });
    },
    filteredVenuesWithShows() {
      let filteredVenues = this.venuesWithShows;

      if (this.selectedVenue) {
        filteredVenues = filteredVenues.filter(
          (venue) => venue.place === this.selectedVenue
        );
      }
      if (this.selectedTag) {
        filteredVenues = filteredVenues.map((venue) => {
          return {
            ...venue,
            shows: venue.shows.filter((show) =>
              show.tags.split(",").includes(this.selectedTag)
            ),
          };
        });
      }

      return filteredVenues;
    },
  },
  mounted() {
    this.get_shows();
  },
};
</script>
