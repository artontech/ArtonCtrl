import { createRouter, createWebHistory } from "vue-router";
import routes from "./routes";
const routerBase = import.meta.env.VITE_ROUTER_BASE;

const router = createRouter({
  history: createWebHistory(routerBase),
  routes,
});

export default router;
