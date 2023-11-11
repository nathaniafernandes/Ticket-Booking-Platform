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
        <a class="navbar-brand text-white" href="http://localhost:8080"
          >Save A Seat</a
        >
      </div>
    </nav>
    <div class="row justify-content-center mt-5">
      <div class="card p-4">
        <div class="d-flex flex-column align-items-center">
          <img
            :src="require('@/assets/SAS-3.jpeg')"
            alt="App Logo"
            height="165"
          />
        </div>
        <div class="card-body">
          <ul class="nav nav-tabs" role="tablist">
            <li class="nav-item" role="presentation">
              <a
                class="nav-link"
                :class="{ active: activeTab === 'user' }"
                @click="activeTab = 'user'"
              >
                User Login
              </a>
            </li>
            <li class="nav-item">
              <a
                class="nav-link"
                :class="{ active: activeTab === 'admin' }"
                @click="activeTab = 'admin'"
              >
                Admin Login
              </a>
            </li>
          </ul>

          <div v-if="activeTab === 'user'" class="form-container">
            <form @submit.prevent="loginUser">
              <div class="form-group">
                <label for="username">Username</label>
                <input
                  type="text"
                  class="form-control"
                  id="username"
                  v-model="user.username"
                  required
                />
              </div>
              <div class="form-group">
                <label for="email">Email</label>
                <input
                  type="email"
                  class="form-control"
                  id="email"
                  v-model="user.email"
                  required
                />
              </div>
              <div class="form-group">
                <label for="password">Password</label>
                <input
                  type="password"
                  class="form-control"
                  id="password"
                  v-model="user.password"
                  required
                />
                <div class="text-center">
                  <a href="http://localhost:8080/register">New User? SignUp.</a>
                </div>
              </div>
              <div class="text-center">
                <button type="submit" class="btn btn-primary">Login</button>
              </div>
            </form>
          </div>

          <div v-if="activeTab === 'admin'" class="form-container">
            <form @submit.prevent="loginAdmin">
              <div class="form-group">
                <label for="id">ID</label>
                <input
                  type="text"
                  class="form-control"
                  id="id"
                  v-model="admin.id"
                  required
                />
              </div>
              <div class="form-group">
                <label for="username">Username</label>
                <input
                  type="text"
                  class="form-control"
                  id="username"
                  v-model="admin.username"
                  required
                />
              </div>
              <div class="form-group">
                <label for="password">Password</label>
                <input
                  type="password"
                  class="form-control"
                  id="password"
                  v-model="admin.password"
                  required
                />

                <div class="text-center">
                  <a>.</a>
                </div>
              </div>
              <div class="text-center">
                <button type="submit" class="btn btn-primary">Login</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.form-container form {
  height: 310px;
}
</style>

<script>
import axios from "axios";
export default {
  name: "loginVue",
  data() {
    return {
      activeTab: "user",
      user: {
        username: "",
        email: "",
        password: "",
      },
      admin: {
        id: 0,
        username: "",
        password: "",
      },
    };
  },
  methods: {
    loginUser() {
      const userData = {
        username: this.user.username,
        email: this.user.email,
        password: this.user.password,
      };
      axios
        .post("http://localhost:5000/login/user", userData)
        .then((response) => {
          if (response.data.access_token) {
            localStorage.setItem("access_token", response.data.access_token);
            alert("Login successful!");
            this.$router.push({
              path: "/explore",
              query: { userId: response.data.ID },
            });
          } else {
            alert(response.data.message);
          }
        })
        .catch((error) => {
          if (
            error.response &&
            error.response.data &&
            error.response.data.message
          ) {
            this.errorMessage = error.response.data.message;
          } else {
            this.errorMessage = "Login failed. Please check your credentials.";
          }
        });
    },

    loginAdmin() {
      const adminData = {
        id: this.admin.id,
        username: this.admin.username,
        password: this.admin.password,
      };
      axios
        .post("http://localhost:5000/login/admin", adminData)
        .then((response) => {
          if (response.data.access_token) {
            localStorage.setItem("access_token", response.data.access_token);
            alert("Login successful!");
            this.$router.push({
              path: "/admindashboard",
              query: { userId: response.data.ID },
            });
          } else {
            alert(response.data.message);
          }
        })
        .catch((error) => {
          // Login failed
          if (
            error.response &&
            error.response.data &&
            error.response.data.message
          ) {
            this.errorMessage = error.response.data.message;
          } else {
            this.errorMessage = "Login failed. Please check your credentials.";
          }
        });
    },
    getReponse() {
      const path = "http://localhost:5000/";
      axios
        .get(path)
        .then((res) => {
          console.log(res.data);
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  created() {
    this.getReponse();
  },
};
</script>
