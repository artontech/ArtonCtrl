import { createApp } from "vue";

import App from "@/App.vue";
import Router from "@/router/index";
import Store from "@/store/index";

import "@/style.css";

const app = createApp(App);
app.use(Router).use(Store).mount("#app");
