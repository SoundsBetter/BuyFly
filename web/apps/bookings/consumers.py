import json

from channels.generic.websocket import AsyncWebsocketConsumer


class TicketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ticket_id = self.scope['url_route']['kwargs']['ticket_id']
        self.ticket_group = f"ticket_{self.ticket_id}"

        await self.channel_layer.group_add(
            self.ticket_group, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.ticket_group, self.channel_name
        )

    async def ticket_update(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))