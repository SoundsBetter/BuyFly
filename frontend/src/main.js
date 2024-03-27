import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'
import axios from "axios";
import VueCookies from "vue3-cookies";

axios.defaults.baseURL = 'http://localhost:8000/api/v1/';
axios.defaults.withCredentials = true;

// Додавання інтерсептора відповіді для обробки помилок авторизації
axios.interceptors.response.use(response => {
  // Просто передаємо відповідь, якщо все в порядку
  return response;
}, error => {
  // Перевірка на статус код 401 (неавторизовано)
  if (error.response && error.response.status === 401) {
    // Спроба оновлення токена за допомогою рефреш-токена
    const refreshToken = VueCookies.cookies.get('refresh_token');

    if (refreshToken) {
      return axios.post('/refresh', { refresh: refreshToken })
        .then(res => {
          // Оновлення токена доступу
          VueCookies.cookies.set('access_token', res.data.access, "1d");
          // Оновлення заголовка Authorization для повторного запиту
          error.config.headers['Authorization'] = `Bearer ${res.data.access}`;
          // Повторний запит з оновленим токеном
          return axios(error.config);
        }).catch(refreshError => {
          // Обробка помилки оновлення токена
          console.error('Error refreshing token:', refreshError);
          // Можливо, перенаправлення на сторінку входу
          return Promise.reject(refreshError);
        });
    }
  }
  // Передати помилку далі, якщо не 401 або немає рефреш-токена
  return Promise.reject(error);
});


const app = createApp(App)
app.use(router)
app.use(VueCookies, {
  expireTimes: "1d",
  path: "/",
  domain: "",
  secure: false,
  sameSite: "None"
})
app.mount('#app')