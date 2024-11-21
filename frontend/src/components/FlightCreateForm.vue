<script setup>
import {ref, onMounted} from 'vue';
import API from "@/api/api";
import {fetchAirports} from "@/services/airportService";

const departureAirport = ref(null);
const arrivalAirport = ref(null);
const airports = ref([]);
const status = ref("scheduled");
const departureDatetime = ref("2024-03-28T14:39");
const duration = ref("02:00:00");
const basePrice = ref("100");
const optionsPriceCoefficient = ref("1");
const options = ref([]);

onMounted(async () => {
  airports.value = await fetchAirports();
});

const findOrCreateRoute = async () => {
  try {
    const routeResponse = await API.get(`flights/routes/search/?departure_airport=${departureAirport.value.id}&arrival_airport=${arrivalAirport.value.id}`);
    if (routeResponse.data.length === 0) {
      const createRouteResponse = await API.post(`flights/routes/`, {
        departure_airport: departureAirport.value.icao,
        arrival_airport: arrivalAirport.value.icao
      });
      return createRouteResponse.data.id;
    } else {
      console.log(routeResponse)
      return routeResponse.data[0].id;
    }
  } catch (error) {
    console.error('Error in finding or creating route:', error);
    throw error;
  }
};

const createFlight = async () => {
  try {
    const routeId = await findOrCreateRoute();
    const response = await API.post(`flights/`, {
      route: routeId,
      status: status.value,
      departure_datetime: departureDatetime.value,
      duration: duration.value,
      base_price: basePrice.value,
      options_price_coefficient: optionsPriceCoefficient.value,
      options: options.value
    });
    alert('Flight successfully created!');
    console.log('Created flight:', response.data);
  } catch (error) {
    console.log(error.response.data)
    console.error('Error in creating flight:', error);
  }
};
</script>

<template>
  <div class="container mt-5">
    <h2>Create Flight</h2>
    <form @submit.prevent="createFlight" class="needs-validation" novalidate>
      <div class="mb-3">
        <label class="form-label" for="departureAirport">Departure
          Airport:</label>
        <select class="form-select" v-model="departureAirport">
          <option v-for="airport in airports" :key="airport.id"
                  :value="airport">
            {{ airport.name }}
          </option>
        </select>
      </div>
      <div class="mb-3">
        <label class="form-label" for="arrivalAirport">Arrival Airport:</label>
        <select class="form-select" v-model="arrivalAirport">
          <option v-for="airport in airports" :key="airport.id"
                  :value="airport">
            {{ airport.name }}
          </option>
        </select>
      </div>
      <div class="mb-3">
        <label class="form-label" for="status">Status:</label>
        <select class="form-select" v-model="status">
          <option value="scheduled">Scheduled</option>
        </select>
      </div>
      <div class="mb-3">
        <label class="form-label" for="departureDatetime">Departure
          Datetime:</label>
        <input class="form-control" type="datetime-local"
               v-model="departureDatetime"/>
      </div>
      <div class="mb-3">
        <label class="form-label" for="duration">Duration (HH:MM):</label>
        <input class="form-control" type="text" v-model="duration"/>
      </div>
      <div class="mb-3">
        <label class="form-label" for="basePrice">Base Price:</label>
        <input class="form-control" type="number" step="0.01"
               v-model="basePrice"/>
      </div>
      <div class="mb-3">
        <label class="form-label" for="optionsPriceCoefficient">Options Price
          Coefficient:</label>
        <input class="form-control" type="number" step="0.00001"
               v-model="optionsPriceCoefficient"/>
      </div>
      <button type="submit" class="btn btn-success">Створити рейс</button>
    </form>
  </div>
</template>


