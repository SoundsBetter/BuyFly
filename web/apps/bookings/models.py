from django.db import models
from django.conf import settings


class Booking(models.Model):
    class Status(models.TextChoices):
        RESERVED = 'reserved'
        PENDING = 'pending'
        APPROVED = 'approved'
        COMPLETED = 'completed'
        CANCELLED = 'cancelled'

    flight = models.ForeignKey(
        "flights.Flight",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    number = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=32, choices=Status.choices, default=Status.RESERVED
    )




class Passenger(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)


class Ticket(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending'
        CHECK_IN = 'check_in'
        BOARDED = 'boarded'
        CANCELLED = 'cancelled'
        REFUNDED = 'refunded'

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    seat = models.ForeignKey("flights.Seat", on_delete=models.SET_NULL, null=True)

    status = models.CharField(
        max_length=32, choices=Status.choices, default=Status.PENDING
    )


class Option(models.Model):
    name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=20, decimal_places=2)


