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
    <div class="container d-flex justify-content-center mt-5">
      <div class="card p-4">
        <h2>User Registration</h2>
        <div v-if="errorMessage" class="alert alert-danger">
          {{ errorMessage }}
        </div>
        <form @submit.prevent="registerUser">
          <div class="form-group">
            <label for="username">Username</label>
            <input
              type="text"
              class="form-control"
              v-model="username"
              required
            />
          </div>
          <div class="form-group">
            <label for="email">Email</label>
            <input type="email" class="form-control" v-model="email" required />
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <input
              type="password"
              class="form-control"
              v-model="password"
              required
            />
          </div>
          <button type="submit" class="btn btn-primary">Register</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "userRegister",
  data() {
    return {
      username: "",
      email: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    registerUser() {
      const userData = {
        username: this.username,
        email: this.email,
        password: this.password,
      };

      axios
        .post("http://localhost:5000/register", userData)
        .then((response) => {
          console.log(response);
          this.$router.push("/");
        })
        .catch((error) => {
          if (
            error.response &&
            error.response.data &&
            error.response.data.message
          ) {
            this.errorMessage = error.response.data.message;
          } else {
            this.errorMessage = "Registration failed. Please try again later.";
          }
        });
    },
  },
};
</script>
