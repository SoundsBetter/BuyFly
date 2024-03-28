<template>
  <div v-if="ticket">
    <h1>Ticket detail</h1>
    <TicketData :ticket="ticket" />
  </div>
</template>

<script setup>
import TicketData from './TicketData.vue';
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const ticket = ref(null);

onMounted(() => {
  const ticketId = route.params.id;
  const webSocketUrl = `ws://localhost:8000/ws/ticket/${ticketId}/`;
  const chatSocket = new WebSocket(webSocketUrl);

  chatSocket.onopen = function(e) {
    console.log('WebSocket connection established for ticket', ticketId);
  };

  chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data && data.ticket_id && data.ticket_id === ticketId) {
      ticket.value = { ...ticket.value, ...data };
    }
  };

  chatSocket.onclose = function(e) {
    console.error('WebSocket connection closed unexpectedly');
  };

  chatSocket.onerror = function(e) {
    console.error('WebSocket encountered an error:', e);
  };
});
</script>
