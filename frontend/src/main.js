import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'
import axios from "axios";
import store from "@/store";

axios.defaults.baseURL = 'http://localhost:8000/api/v1/';
axios.defaults.withCredentials = true;


axios.interceptors.response.use(
  response => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !store.state.isRefreshing) {
      store.dispatch('startTokenRefresh'); // Початок процесу оновлення

      try {
        await axios.post('accounts/token/refresh/', {});
        return axios(originalRequest);
      } catch (refreshError) {
        store.dispatch('finishTokenRefresh');
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

const app = createApp(App)

app.use(router)

app.mount('#app')