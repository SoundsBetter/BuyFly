<template>
  <div>
    <h1>Ticket list</h1>
    <TicketData v-for="ticket in tickets" :key="ticket.id" :ticket="ticket" />
  </div>
</template>

<script setup>
import TicketData from './TicketData.vue';
import { ref, onMounted } from 'vue';

const tickets = ref([]);

onMounted(() => {
  // Припустимо, що URL вашого веб-сокету - це ws://localhost:8000/ws/tickets/
  const webSocketUrl = `ws://localhost:8000/ws/tickets/`;
  const chatSocket = new WebSocket(webSocketUrl);

  chatSocket.onopen = function() {
    console.log('WebSocket connection established');
    chatSocket.send(JSON.stringify({
      command: 'subscribe',
      // ticket_ids може бути отримано з сервера або іншого джерела
      ticket_ids: tickets.value.map(ticket => ticket.id)
    }));
  };

  chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.ticket_id) {
      const index = tickets.value.findIndex(ticket => ticket.id === data.ticket_id);
      if (index !== -1) {
        tickets.value[index] = { ...tickets.value[index], ...data };
      }
    }
  };

  chatSocket.onclose = function() {
    console.error('WebSocket connection closed unexpectedly');
  };

  chatSocket.onerror = function() {
    console.error('WebSocket encountered an error:');
  };
});
</script>
