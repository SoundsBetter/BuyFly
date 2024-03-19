from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from liqpay import LiqPay
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings

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
from .services import create_payment_for_booking


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

    @action(detail=True, methods=["get"], url_path="calculate_price")
    def calculate_price(self, request, pk=None):
        try:
            Booking.objects.calculate_price(booking_id=pk)
        except Booking.DoesNotExist:
            return Response(
                {"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {"message": "Booking price is calculated"}, status=status.HTTP_200_OK
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

    @action(detail=True, methods=["get"], url_path="calculate_price")
    def calculate_price(self, request, pk=None):
        try:
            Ticket.objects.calculate_price(ticket_id=pk)
        except Ticket.DoesNotExist:
            return Response(
                {"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {"message": "Ticket price is calculated"}, status=status.HTTP_200_OK
        )



class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [IsAuthenticated, IsSupervisor | IsCheckInManager]


class TicketOptionViewSet(viewsets.ModelViewSet):
    serializer_class = TicketOptionSerializer
    permission_classes = [
        IsAuthenticated,
        IsSupervisor | IsCheckInManager | IsOwner,
    ]

    def perform_create(self, serializer):
        ticket_id = self.kwargs.get("ticket_pk")
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        serializer.save(ticket=ticket)

    def get_queryset(self):
        return TicketOption.objects.filter(ticket_id=self.kwargs["ticket_pk"])


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        if self.request.user.groups.filter(name="supervisors").exists():
            return Payment.objects.all()
        return Payment.objects.filter(passenger__user=self.request.user)


@method_decorator(csrf_exempt, name='dispatch')
class LiqPayCallbackAPIView(APIView):
    def post(self, request, *args, **kwargs):
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        data = request.data.get('data')
        signature = request.data.get('signature')
        sign = liqpay.str_to_sign(
            settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY)

        if sign == signature:
            print('callback is valid')
            response = liqpay.decode_data_from_str(data)
            print('callback data', response)
            return Response({'status': 'success', 'data': response})
        else:
            return Response({'status': 'error', 'message': 'Invalid signature'},
                            status=400)
