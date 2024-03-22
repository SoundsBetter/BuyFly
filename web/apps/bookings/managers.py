import secrets
from datetime import datetime
from django.db import models

from .conf import BOOKING_NUMBER_TEMPLATE, BUSINESS_COEFFICIENT, \
    TICKET_NUMBER_TEMPLATE


class BookingManager(models.Manager):
    def create_booking_number(self, user, flight):
        date_str = datetime.now().strftime("%y%m%H%M%S")
        token = secrets.token_hex(2)
        number = BOOKING_NUMBER_TEMPLATE.format(
            user_pk=user.pk, flight_id=flight.id, date=date_str, token=token
        )
        return number

    def calculate_price(self, booking_id):
        booking = self.get(pk=booking_id)
        booking.price = sum(
            ticket.price for ticket in self.get(pk=booking_id).tickets.all()
        )
        booking.save()


class TicketManager(models.Manager):
    def get_available_options(self, ticket_pk):
        ticket = self.get(pk=ticket_pk)
        return ticket.booking.flight.options.all()

    def calculate_price(self, ticket_id):
        ticket = self.get(pk=ticket_id)
        base_price = ticket.booking.flight.base_price
        options_price_coefficient = (
            ticket.booking.flight.options_price_coefficient
        )
        if ticket.seat_type == "B":
            flight_price = base_price * BUSINESS_COEFFICIENT
        else:
            flight_price = base_price
        options_price = sum(
            option.price * options_price_coefficient
            for option in ticket.options.all()
        )
        ticket.price = flight_price + options_price
        ticket.save()

    def create_ticket_number(self, booking):
        token = secrets.token_hex(3)
        number = TICKET_NUMBER_TEMPLATE.format(
            token=token, booking_id=booking.id
        )
        return number
