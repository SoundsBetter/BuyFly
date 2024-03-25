from django.urls import re_path
from .consumers import TicketConsumer, TicketListConsumer

websocket_urlpatterns = [
    re_path(r'ws/ticket/(?P<ticket_id>\w+)/$', TicketConsumer.as_asgi()),
    re_path("ws/tickets/", TicketListConsumer.as_asgi()),
]
