from django.db import models
from django.conf import settings
from django.db.models import UniqueConstraint

from apps.flights.models import SeatType
from .managers import TicketManager, BookingManager


class Booking(models.Model):
    objects = BookingManager()

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

    price = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True
    )
    number = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=32, choices=Status.choices, default=Status.RESERVED
    )

    def __str__(self):
        return f"{self.pk} - {self.number}"




class Passenger(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    date_of_birth = models.DateField()
    passport_number = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.passport_number}"


class Ticket(models.Model):
    objects = TicketManager()

    class Status(models.TextChoices):
        PENDING = 'pending'
        CHECK_IN = 'check_in'
        BOARDED = 'boarded'
        CANCELLED = 'cancelled'
        REFUNDED = 'refunded'

    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name='tickets'
    )
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    seat = models.ForeignKey("flights.Seat", on_delete=models.SET_NULL, null=True)

    price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    seat_type = models.CharField(max_length=32, choices=SeatType.choices)
    status = models.CharField(
        max_length=32, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Option(models.Model):
    name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"{self.name} for {self.price}"


class TicketOption(models.Model):
    option = models.ForeignKey(
        "Option", on_delete=models.CASCADE
    )
    ticket = models.ForeignKey(
        "Ticket", on_delete=models.CASCADE, related_name="options"
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['option', 'ticket'], name='ticket_option')
        ]

    def save(self, *args, **kwargs):
        self.price = self.option.price * self.quantity
        super().save(*args, **kwargs)


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
    status = models.CharField(choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


