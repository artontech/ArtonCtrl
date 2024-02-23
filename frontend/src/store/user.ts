const user = {
  state: {
    user: {
      address: `${window.location.protocol}//${window.location.hostname}:13314`,
      cache: false,
      password: "",
      token: "",
      username: "",
    },
  },
  mutations: {
    user(state, payload) {
      Object.assign(state.user, payload);
    },
  },
};

export default user;
