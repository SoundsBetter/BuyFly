from django.urls import re_path
from .consumers import TicketConsumer

websocket_urlpatterns = [
    re_path(r'ws/ticket/(?P<ticket_id>\w+)/$', TicketConsumer.as_asgi()),
]

