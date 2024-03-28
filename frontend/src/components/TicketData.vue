<template>
  <div class="ticket" :data-ticket-id="ticket.id">
    <div class="container mt-5">
      <div class="card">
        <div class="card-header">
          Ticket <span class="ticket-number">#{{ ticket.number }}</span>
        </div>
        <ul class="list-group list-group-flush">
          <li class="list-group-item">Passenger Name: <span
              class="passenger-name">{{ ticket.passenger.first_name }} {{ ticket.passenger.last_name }}</span>
          </li>
          <li class="list-group-item">Seat Number: <span class="seat-number">{{ ticket.seat ? ticket.seat.number : 'N/A' }}</span></li>
          <li class="list-group-item">Price: <span class="price">{{ ticket.price }}</span></li>
          <li class="list-group-item">Seat Type: <span class="seat-type">{{ ticket.seat_type }}</span></li>
          <li class="list-group-item">Status: <span class="status">{{ ticket.status }}</span></li>
        </ul>
      </div>
    </div>
  </div>
</template>

<!--<script setup>-->
<!--defineProps({-->
<!--  ticket: Object-->
<!--});-->
<!--</script>-->

<style scoped>
</style>
