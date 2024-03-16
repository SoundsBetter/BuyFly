from django.db import models
from django.conf import settings
from django.db.models import UniqueConstraint

from apps.bookings.managers import TicketManager


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
    objects = TicketManager()

    class Status(models.TextChoices):
        PENDING = 'pending'
        CHECK_IN = 'check_in'
        BOARDED = 'boarded'
        CANCELLED = 'cancelled'
        REFUNDED = 'refunded'

    options = models.ManyToManyField(
        "Option",
        through='TicketOption',
        related_name='tickets'
    )

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    seat = models.ForeignKey("flights.Seat", on_delete=models.SET_NULL, null=True)

    status = models.CharField(
        max_length=32, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Option(models.Model):
    name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=20, decimal_places=2)


class TicketOption(models.Model):
    option = models.ForeignKey(
        "Option", on_delete=models.CASCADE
    )
    ticket = models.ForeignKey(
        "Ticket", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['option', 'ticket'], name='ticket_option')
        ]


class PaymentMethod(models.Model):
    pass


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending'
        APPROVED = 'approved'
        REJECTED = 'rejected'

    booking = models.ForeignKey(
        "Booking", on_delete=models.CASCADE, related_name='payments'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


