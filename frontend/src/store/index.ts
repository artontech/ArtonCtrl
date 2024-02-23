import { createStore } from "vuex";

import cachePlugin from "./cache-plugin";
import user from "./user";

const store = createStore({
  plugins: [cachePlugin],
  state: {
    ...user.state,
  },
  mutations: {
    update(state, payload) {
      Object.assign(state, payload);
    },
    ...user.mutations,
  },
});

export default store;
