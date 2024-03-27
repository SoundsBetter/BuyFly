<template>
  <div>
    <AlertMessage :message="message" :type="messageType"/>
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
    </form>
  </div>
</template>

<script>
import AlertMessage from '@/components/AlertMessage.vue';
import axios from 'axios';

export default {
  components: {
    AlertMessage
  },
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
        await axios.post('accounts/registration/', data);
        this.message = 'Registration successful!';
        this.messageType = 'success';
      } catch (error) {
        if (error.response && error.response.data) {
          this.message = Object.keys(error.response.data).map(key => {
            const errors = error.response.data[key];
            return `${key}: ${errors.join(', ')}`;
          }).join('; ');
          this.messageType = 'danger';
        } else {
          this.message = 'Something went wrong';
          this.messageType = 'danger';
        }
      }
    }
  }
};
</script>
