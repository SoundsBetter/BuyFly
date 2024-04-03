<template>
  <div>
    <h5>Flights:</h5>
    <div>
      <FlightData v-for="flight in flights"
                  :key="flight.id"
                  :flight="flight"
      />
    </div>
  </div>
</template>

<script setup>
import FlightData from "@/components/FlightData.vue";
import {defineProps} from 'vue';

defineProps({
  flights: Array,
});
</script>
