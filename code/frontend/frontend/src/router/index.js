import Vue from "vue";
import VueRouter from "vue-router";
import loginVue from "../components/login.vue";
import UserExplore from "../components/user_explore.vue";
import BookShow from "../components/BookShow.vue";
import adminDashboard from "../components/admindash.vue";
import addVenue from "../components/addvenue.vue";
import addShow from "../components/addShow.vue";
import editVenue from "../components/editVenue.vue";
import editShow from "../components/editShow.vue";
import userRegister from "../components/userRegister.vue";
import UserBookings from "../components/bookings.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "loginVue",
    component: loginVue,
  },
  {
    path: "/explore",
    name: "UserExplore",
    component: UserExplore,
  },
  {
    path: "/BookShow",
    name: "BookShow",
    component: BookShow,
  },
  {
    path: "/adminDashboard",
    name: "adminDashboard",
    component: adminDashboard,
  },
  {
    path: "/addVenue",
    name: "addVenue",
    component: addVenue,
  },
  {
    path: "/addShow",
    name: "addShow",
    component: addShow,
  },
  {
    path: "/editVenue",
    name: "editVenue",
    component: editVenue,
  },
  {
    path: "/editShow",
    name: "editShow",
    component: editShow,
  },
  {
    path: "/register",
    name: "userRegister",
    component: userRegister,
  },
  {
    path: "/bookings",
    name: "UserBookings",
    component: UserBookings,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
