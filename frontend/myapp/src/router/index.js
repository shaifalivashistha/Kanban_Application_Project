import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import DashboardView from "../views/DashboardView.vue";
import createTaskView from "../views/createTaskView.vue";
import createCardView from "../views/createCardView.vue"

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
  {
    path: "/login_page",
    name: "login",
    component: LoginView,
  },
  {
    path: "/register",
    name: "register",
    component: RegisterView,
  },
  {
    path: "/dashboard/:username",
    name: "dashboard",
    component: DashboardView,
  },
  {
    path: "/dashboard/:username/create_list",
    name: "create_list",
    component: createTaskView,
  },
  {
    path: "/:username/:listID/create_card",
    name: "create_card",
    component: createCardView,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
