from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.permissions import (
    IsOwner,
    IsSupervisor,
    IsGateManager,
    IsCheckInManager,
)
from .models import Booking, Passenger, Ticket, Option, TicketOption, Payment
from .serializers import (
    BookingSerializer,
    PassengerSerializer,
    TicketSerializer,
    OptionSerializer,
    TicketOptionSerializer,
    PaymentSerializer,
)


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.groups.filter(name="supervisors").exists():
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        flight = serializer.validated_data["flight"]
        number = Booking.objects.create_booking_number(user=user, flight=flight)
        serializer.save(user=user, number=number)

    def update(self, request, *args, **kwargs):
        booking = self.get_object()
        if booking.status in ["reserved", "pending"]:
            return super().update(request, *args, **kwargs)
        return Response(
            {"detail": "Booking cannot be updated at this stage."},
            status=status.HTTP_403_FORBIDDEN,
        )

    def destroy(self, request, *args, **kwargs):
        booking = self.get_object()
        if booking.status in ["reserved", "pending"]:
            return super().destroy(request, *args, **kwargs)
        return Response(
            {"detail": "Booking cannot be cancelled at this stage."},
            status=status.HTTP_403_FORBIDDEN,
        )


class PassengerViewSet(viewsets.ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    permission_classes = [IsOwner, IsAuthenticated]

    def get_queryset(self):
        return Passenger.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            permission_classes = [
                IsAuthenticated,
                IsSupervisor | IsGateManager | IsCheckInManager | IsOwner,
            ]
        else:
            permission_classes = [
                IsAuthenticated,
                IsSupervisor | IsGateManager | IsCheckInManager,
            ]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.groups.filter(name="supervisors").exists():
            return Ticket.objects.all()
        return Ticket.objects.filter(passenger__user=self.request.user)


class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [IsAuthenticated, IsSupervisor | IsCheckInManager]


class TicketOptionViewSet(viewsets.ModelViewSet):
    queryset = TicketOption.objects.all()
    serializer_class = TicketOptionSerializer
    permission_classes = [
        IsAuthenticated,
        IsSupervisor | IsCheckInManager | IsOwner,
    ]

    def perform_create(self, serializer):
        ticket_id = self.kwargs.get("ticket_pk")
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        serializer.save(ticket=ticket)


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            permission_classes = [
                IsAuthenticated,
                IsSupervisor | IsGateManager | IsCheckInManager | IsOwner,
            ]
        else:
            permission_classes = [
                IsAuthenticated,
                IsSupervisor | IsGateManager | IsCheckInManager,
            ]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.groups.filter(name="supervisors").exists():
            return Payment.objects.all()
        return Payment.objects.filter(passenger__user=self.request.user)


