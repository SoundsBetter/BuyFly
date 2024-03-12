from django.db import models


class Flight(models.Model):
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
    seat_type = models.TextField(choices=SeatType)
    price_coefficient = models.DecimalField(max_digits=20, decimal_places=5)


class Airport(models.Model):
    name = models.CharField(max_length=256)
    code_name = models.CharField(max_length=10, unique=True)
    city = models.CharField(max_length=256)
    country = models.CharField(max_length=256)
