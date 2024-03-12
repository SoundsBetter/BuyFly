from django.db import models


class Flight(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', 'Scheduled'
        ON_TIME = 'on_time', 'On Time'
        DELAYED = 'delayed', 'Delayed'
        BOARDING = 'boarding', 'Boarding'
        DEPARTED = 'departed', 'Departed'
        IN_FLIGHT = 'in_flight', 'In Flight'
        LANDED = 'landed', 'Landed'
        CANCELLED = 'cancelled', 'Cancelled'
        DIVERTED = 'diverted', 'Diverted'
        COMPLETED = 'completed', 'Completed'

    departure_airport = models.ForeignKey(
        "Airport",
        on_delete=models.CASCADE,
        related_name='departure_flights'
    )
    arrival_airport = models.ForeignKey(
        "Airport",
        on_delete=models.CASCADE,
        related_name='arrival_flights'
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.SCHEDULED,
    )

    options = models.ManyToManyField("bookings.Option")

    number = models.CharField(max_length=10, unique=True)
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    base_price = models.DecimalField(max_digits=20, decimal_places=2)
    options_price_coefficient = models.DecimalField(
        max_digits=20, decimal_places=5
    )


class AirplaneType(models.Model):
    model = models.CharField(max_length=10, unique=True)
    params = models.JSONField()


class Airplane(models.Model):
    type = models.ForeignKey(
        "AirplaneType", on_delete=models.CASCADE, related_name='airplane'
    )

    number = models.CharField(max_length=10, unique=True)


class Seat(models.Model):
    airplane = models.ForeignKey(
        "Airplane", on_delete=models.CASCADE, related_name='seats'
    )

    class SeatType(models.TextChoices):
        E = "Economy"
        B = "Business"

    number = models.CharField(max_length=10)
    seat_type = models.CharField(max_length=32, choices=SeatType.choices)
    price_coefficient = models.DecimalField(max_digits=20, decimal_places=5)


class Airport(models.Model):
    class DaylightSavingsTime(models.TextChoices):
        EUROPE = "E"
        US_CANADA = "A"
        SOUTH_AMERICA = "S"
        AUSTRALIA = "O"
        NEW_ZEALAND = "Z"
        NONE = "N"
        UNKNOWN = "U"

    name = models.CharField(max_length=256)
    city = models.CharField(max_length=32, blank=True, null=True)
    country = models.CharField(max_length=32)
    iata = models.CharField(max_length=5, unique=True, null=True)
    icao = models.CharField(max_length=7, unique=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    altitude = models.IntegerField()
    timezone_offset = models.FloatField(null=True, blank=True)
    dst = models.CharField(
        max_length=2,
        choices=DaylightSavingsTime,
        default=DaylightSavingsTime.UNKNOWN
    )
