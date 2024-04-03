<template>
  <div>
    <FlightSearchForm @search="handleSearch" />
    <FlightList :flights="flights" />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import FlightSearchForm from '@/components/FlightSearchForm.vue';
import FlightList from '@/components/FlightList.vue';
import API from '@/api/api.js';

const flights = ref([]);

const handleSearch = async (searchQuery) => {
  try {
    const response = await API.get('flights/', { params: searchQuery });
    console.log(response.data)
    flights.value = response.data;
  } catch (error) {
    console.error("error", error);
    flights.value = [];
  }
};
</script>
