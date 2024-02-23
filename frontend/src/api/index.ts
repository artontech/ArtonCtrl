import axios from "axios";

// axios.defaults.withCredentials = true;

export async function get(
  url: string,
  store,
  withCredentials = true
) {
  const resp = await axios
    .get(store.state.user.address + url, {
      withCredentials,
      headers: {
        token: store.state.user.token,
      },
    })
    .catch((err) => {
      if (err.response.status == 401) {
        window.location.href = "/";
      }
      return err.response.data;
    });
  if (resp.status != 200) throw resp.status;
  if (resp.data?.status != "ok") throw resp.data;
  return resp.data.data;
}

export async function post(
  url: string,
  store,
  data: any,
  withCredentials = true
) {
  const resp = await axios
    .post(store.state.user.address + url, data, {
      withCredentials,
      headers: {
        token: store.state.user.token,
      },
    })
    .catch((err) => {
      if (err.response.status == 401) {
        window.location.href = "/";
      }
      return err.response.data;
    });
  if (resp.status != 200) throw resp.status;
  if (resp.data?.status != "ok") throw resp.data;
  return resp.data.data;
}
