import { post } from "@/api";

interface UserLoginReq {
  username: string;
  password: string;
}

async function login(store, data: UserLoginReq) {
  return post("/login", store, data);
}

export default {
  login,
};
