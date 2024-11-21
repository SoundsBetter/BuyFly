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


class TicketListConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "subscribed_tickets"):
            for ticket_group in self.subscribed_tickets:
                await self.channel_layer.group_discard(
                    ticket_group, self.channel_name
                )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']

        if command == "subscribe":
            ticket_ids = text_data_json['ticket_ids']
            self.subscribed_tickets = [
                f"ticket_{ticket_id}" for ticket_id in ticket_ids
            ]

            for ticket_group in self.subscribed_tickets:
                await self.channel_layer.group_add(
                    ticket_group, self.channel_name
                )

    async def ticket_update(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))
