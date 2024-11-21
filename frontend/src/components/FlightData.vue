<template>
  <div class="card mb-3">
    <div class="card-header">
      Flight {{ flight.number }}
    </div>
    <div class="card-body">
      <h5 class="card-title">{{ flight.route_data.departure_airport }} - {{ flight.route_data.arrival_airport }}</h5>
      <p class="card-text">Status: {{ flight.status }}</p>
      <p class="card-text">Departure: {{ formatDate(flight.departure_datetime) }}</p>
      <p class="card-text">Arrival: {{ formatDate(flight.arrival_datetime) }}</p>
      <p class="card-text">Duration: {{ flight.duration }}</p>
      <p class="card-text">Base Price: ${{ flight.base_price }}</p>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

defineProps({
  flight: Object,
});

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
  return new Date(dateString).toLocaleDateString(undefined, options);
};
</script>

<style scoped>
</style>
