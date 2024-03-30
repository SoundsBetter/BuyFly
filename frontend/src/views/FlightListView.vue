<template>
  <div>
    <h2>Flight List</h2>

    <div><FlightData v-for="flight in flights"
      :key="flight.id"
      :flight="flight"
    /></div>
  </div>
</template>

<script setup>
import FlightData from "@/components/FlightData.vue";
import { ref, onMounted } from 'vue';
import axios from 'axios';

const flights = ref([]);

onMounted(async () => {
  try {
    const response = await axios.get('flights/');
    console.log(response)
    flights.value = response.data;
  } catch (error) {
    console.error(error);
  }
});
</script>
