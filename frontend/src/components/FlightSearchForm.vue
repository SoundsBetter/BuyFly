<script setup>
import {ref, defineEmits, onMounted, watch} from 'vue';
import {fetchAirports} from "@/services/airportService";
const airports = ref([]);
const emit = defineEmits(['search'])
const searchQuery = ref({
  departure_airport: 'AYGA',
  arrival_airport: 'AYMD',
  departure_date: '',
});

const searchDeparture = ref('');
const searchArrival = ref('');
const filteredDepartureAirports = ref([]);
const filteredArrivalAirports = ref([]);

onMounted(async () => {
  airports.value = await fetchAirports();
});

const updateFilteredAirports = (searchText, filteredAirports) => {
  if (searchText.length > 1) {
    const searchLower = searchText.toLowerCase();
    filteredAirports.value = airports.value.filter(airport =>
        airport.name.toLowerCase().includes(searchLower)
    ).slice(0, 3);
  } else {
    filteredAirports.value = [];
  }
};

const selectAirport = (airport, type) => {
  if (type === 'departure') {
    searchQuery.value.departure_airport = airport.icao;
    searchDeparture.value = airport.name;
  } else if (type === 'arrival') {
    searchQuery.value.arrival_airport = airport.icao;
    searchArrival.value = airport.name;
  }
  setTimeout(() => {
    filteredDepartureAirports.value = [];
    filteredArrivalAirports.value = [];
  }, 0);
  filteredDepartureAirports.value = [];
  filteredArrivalAirports.value = [];
};

watch(searchDeparture, (newVal) => updateFilteredAirports(newVal, filteredDepartureAirports));
watch(searchArrival, (newVal) => updateFilteredAirports(newVal, filteredArrivalAirports));
const submitSearch = () => {
  emit('search', searchQuery.value);
};

</script>

<template>
  <div class="container mt-5">
    <div class="form-group mb-3 p-4 bg-white rounded shadow">
      <form @submit.prevent="submitSearch" class="row g-3 align-items-end">

        <div class="col-md position-relative">
          <input class="form-control" type="text" v-model="searchDeparture"
                 placeholder="From">
          <ul class="list-group position-absolute w-100"
              v-show="filteredDepartureAirports.length > 0">
            <li class="list-group-item"
                v-for="airport in filteredDepartureAirports" :key="airport.id"
                @click="selectAirport(airport, 'departure')">
              {{ airport.name }}
            </li>
          </ul>
        </div>

        <div class="col-md position-relative">
          <input class="form-control" type="text" v-model="searchArrival"
                 placeholder="To">
          <ul class="list-group position-absolute w-100"
              v-show="filteredArrivalAirports.length > 0">
            <li class="list-group-item"
                v-for="airport in filteredArrivalAirports" :key="airport.id"
                @click="selectAirport(airport, 'arrival')">
              {{ airport.name }}
            </li>
          </ul>
        </div>

        <!--          <div class="col-md">-->
        <!--            <label for="departure_date" class="form-label">Date</label>-->
        <!--            <input id="departure_date" class="form-control"-->
        <!--                   v-model="searchQuery.departure_date" type="date"-->
        <!--                   placeholder="Date" required>-->
        <!--          </div>-->

        <div class="col-md">
          <VDatePicker v-model="searchQuery.departure_date" mode="date"/>
        </div>

        <div class="col-md-auto">
          <button class="btn btn-primary" type="submit">Search</button>
        </div>
      </form>
    </div>
  </div>
</template>

