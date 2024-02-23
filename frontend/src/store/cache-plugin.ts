const cachePlugin = (store) => {
  // Load init value from localStorage
  const initValues = {};
  for (let key in store.state) {
    const value = localStorage.getItem(key);
    if (!value) continue;
    initValues[key] = JSON.parse(value);
  }
  if (Reflect.ownKeys(initValues).length) store.commit("update", initValues);

  // Update localStorage value
  store.subscribe((mutation, _) => {
    const key = mutation.type;
    if (!mutation.payload.cache) {
      localStorage.removeItem(key);
      return;
    }
    const values = JSON.parse(localStorage.getItem(key) || "{}");
    Object.assign(values, mutation.payload);
    localStorage.setItem(key, JSON.stringify(values));
  });
};

export default cachePlugin;
