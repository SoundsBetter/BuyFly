<template>
  <div>
    <form @submit.prevent="register"
          class="needs-validation p-4 border rounded shadow">
      <h2 class="mb-4">Registration</h2>
      <div class="form-group mb-3">
        <label for="username">Username</label>
        <input type="text" class="form-control" id="username" v-model="username"
               placeholder="Enter your username">
      </div>
      <div class="form-group mb-3">
        <label for="email">Email Address</label>
        <input type="email" class="form-control" id="email" v-model="email"
               placeholder="Enter your email">
      </div>
      <div class="form-group mb-3">
        <label for="password1">Password</label>
        <input type="password" class="form-control" id="password1"
               v-model="password1" placeholder="Enter your password">
      </div>
      <div class="form-group mb-4">
        <label for="password2">Confirm Password</label>
        <input type="password" class="form-control" id="password2"
               v-model="password2" placeholder="Confirm your password">
      </div>
      <button type="submit" class="btn btn-primary">Register</button>
      <div v-if="message" class="alert mt-3"
           :class="messageType === 'error' ? 'alert-danger' : 'alert-success'">
        {{ message }}
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: "",
      email: '',
      password1: '',
      password2: '',
      message: '',
      messageType: ''
    };
  },
  methods: {
    async register() {
      const data = {
        username: this.username,
        email: this.email,
        password1: this.password1,
        password2: this.password2,
      };

      try {
        await axios.post('http://localhost:8000/api/v1/accounts/registration/', data);
        this.message = 'Registration successful!';
        this.messageType = 'success';
        // Clear the form or redirect the user
      } catch (error) {
        console.error(error.response.data)
        console.error('!!!!!!!!!!!!!!')
        if (error.response && error.response.data) {
          // Створення рядка з повідомлень про помилки для відображення
          this.message = Object.keys(error.response.data).map(key => {
            const errors = error.response.data[key];
            return `${key}: ${errors.join(', ')}`; // Об'єднуємо масив помилок в один рядок
          }).join('; ');
          this.messageType = 'error';
        } else {
          this.message = 'Сталася помилка під час реєстрації.';
          this.messageType = 'error';
        }
      }
    }
  }
};
</script>
