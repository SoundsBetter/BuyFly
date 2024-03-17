import secrets
from datetime import datetime
from django.db import models

from .conf import BOOKING_NUMBER_TEMPLATE


class BookingManager(models.Manager):
    def create_booking_number(self, user, flight):
        date_str = datetime.now().strftime("%y%m%H%M%S")
        token = secrets.token_hex(2)
        number = BOOKING_NUMBER_TEMPLATE.format(
            user_pk=user.pk, flight_id=flight.id, date=date_str, token=token
        )
        return number


class TicketManager(models.Manager):
    def get_available_options(self, ticket_pk):
        ticket = self.get(pk=ticket_pk)
        return ticket.booking.flight.options.all()


