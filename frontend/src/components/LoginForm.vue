<script setup>
import AlertMessage from '@/components/AlertMessage.vue';
import {ref} from 'vue';
import {useRouter} from 'vue-router';
import AuthService from "@/services/AuthService";

const password = ref('');
const username = ref('');
const message = ref('')
const messageType = ref('')

const router = useRouter()

const login = async () => {
  try {
    const response = await AuthService.login( {
      password: password.value,
      username: username.value,
    });
    console.log('Login successful:', response);
    message.value = "Login successful"
    messageType.value = "success"
    await router.push("/")

  } catch (error) {
    if (error.response && error.response.data) {
      message.value = Object.keys(error.response.data).map(key => {
        const errors = error.response.data[key];
        return `${errors.join(', ')}`;
      }).join('; ');
      messageType.value = 'danger';
    }
  }
};
</script>

<template>
  <AlertMessage :message="message" :type="messageType"/>
  <form @submit.prevent="login"
        class="needs-validation p-4 border rounded shadow">
    <h2 class="mb-4">Log in</h2>
    <div class="form-group mb-3">
      <label for="username">Username</label>
      <input type="username" class="form-control" id="username"
             v-model="username" required
             placeholder="username">
    </div>
    <div class="form-group mb-3">
      <label for="password">Password</label>
      <input type="password" class="form-control" id="password"
             v-model="password" required
             placeholder="password">
    </div>
    <button type="submit" class="btn btn-primary">Login</button>
  </form>
</template>

<style scoped>

</style>