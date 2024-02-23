import { RouteRecordRaw } from "vue-router";
import Ctrl from "@/views/Ctrl.vue";
import Index from "@/views/Index.vue";

const routes: RouteRecordRaw[] = [
  {
    path: "/ctrl",
    name: "Ctrl",
    component: Ctrl,
  },
  {
    path: "/",
    name: "Index",
    component: Index,
  },
];

export default routes;
