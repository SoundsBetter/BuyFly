<script setup>
import {ref} from 'vue';
import AlertMessage from "@/components/AlertMessage.vue";
import AuthService from "@/services/AuthService";

const username = ref("");
const email = ref('');
const password1 = ref('');
const password2 = ref('');
const usernameError = ref('');
const emailError = ref('');
const password1Error = ref('');
const password2Error = ref('');
const message = ref('')
const messageType = ref('')

const clearErrors = () => {
  usernameError.value = '';
  emailError.value = '';
  password1Error.value = '';
  password2Error.value = '';
};

const register = async () => {
  clearErrors();
  try {
    const response = await AuthService.register( {
      username: username.value,
      email: email.value,
      password1: password1.value,
      password2: password2.value,
    });
    console.log('Registration successful:', response);
    message.value = "Registration successful"
    messageType.value = "success"
  } catch (error) {
    if (error.response && error.response.data) {
      Object.keys(error.response.data).forEach(key => {
        const errors = error.response.data[key].join(', ');
        if (key === 'username') {
          usernameError.value = errors;
        } else if (key === 'email') {
          emailError.value = errors;
        } else if (key === 'password1') {
          password1Error.value = errors;
        } else if (key === 'password2') {
          password2Error.value = errors;
        }
      });
    }
  }
};
</script>

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
        <div class="text-danger mt-2">{{ usernameError }}</div>
      </div>
      <div class="form-group mb-3">
        <label for="email">Email Address</label>
        <input type="email" class="form-control" id="email" v-model="email"
               placeholder="Enter your email">
        <div class="text-danger mt-2">{{ emailError }}</div>
      </div>
      <div class="form-group mb-3">
        <label for="password1">Password</label>
        <input type="password" class="form-control" id="password1"
               v-model="password1" placeholder="Enter your password">
        <div class="text-danger mt-2">{{ password1Error }}</div>
      </div>
      <div class="form-group mb-4">
        <label for="password2">Confirm Password</label>
        <input type="password" class="form-control" id="password2"
               v-model="password2" placeholder="Confirm your password">
        <div class="text-danger mt-2">{{ password2Error }}</div>
      </div>
      <button type="submit" class="btn btn-primary">Register</button>
    </form>
  </div>
</template>
