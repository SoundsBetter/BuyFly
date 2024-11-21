import axios from "axios";
import store from "@/store";
import router from "@/router";


const API = axios.create({
    baseURL: 'http://localhost:8000/api/v1/',
    withCredentials: true,
});

API.interceptors.response.use(
  response => response,
  async (error) => {
    const originalRequest = error.config;
    console.log(error)
    if (error.response.status === 401 && !store.state.auth.isRefreshing) {
      console.log(store.state.auth.isRefreshing)
      store.dispatch('auth/startTokenRefresh');
      console.log(store.state.auth.isRefreshing)
      try {
        await API.post('accounts/token/refresh/', {});
        store.dispatch('auth/fetchUserRole');
        return API(originalRequest);
      } catch (refreshError) {
        store.dispatch('auth/finishTokenRefresh');
        await router.push("/")
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default API;
