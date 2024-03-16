from django.db import models

from .conf import COMPANY_CODE_NAME, FLIGHT_NUMBER_TEMPLATE

class FlightManager(models.Manager):
    def create_flight(self, route):
        same_route = self.get_queryset().filter(route=route).count()
        flight_number = FLIGHT_NUMBER_TEMPLATE.format(
            prefix=COMPANY_CODE_NAME,
            route_pk=route.pk,
            counter=same_route + 1
        )
        return flight_number




class AirportManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(icao=None)


