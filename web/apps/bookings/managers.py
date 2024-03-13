from django.db import models


class TicketManager(models.Manager):

    def get_available_options(self, ticket):
        return ticket.booking.flight.options.all()


