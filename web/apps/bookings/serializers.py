from rest_framework import serializers

from apps.flights.models import Flight, Seat
from .models import (
    Booking,
    Passenger,
    Ticket,
    Option,
    TicketOption,
    Payment,
)


class BookingSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    flight = serializers.HyperlinkedRelatedField(
        required=True, view_name="flight-detail", queryset=Flight.objects.all()
    )
    tickets = serializers.HyperlinkedRelatedField(
        many=True, view_name="ticket-detail", read_only=True
    )

    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ["number", "price"]


class PassengerSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Passenger
        fields = "__all__"


class TicketSerializer(serializers.HyperlinkedModelSerializer):
    seat = serializers.HyperlinkedRelatedField(
        queryset=Seat.objects.all(),
        required=False,
        allow_null=True,
        view_name="seat-detail",
    )
    options = serializers.PrimaryKeyRelatedField(
        read_only=True,
        many=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Ticket
        fields = "__all__"
        read_only_fields = ["price", "number"]


class OptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Option
        fields = "__all__"


class TicketOptionSerializer(serializers.ModelSerializer):
    ticket = serializers.HyperlinkedRelatedField(
        view_name="ticket-detail", read_only=True
    )
    option = serializers.PrimaryKeyRelatedField(queryset=Option.objects.none())

    class Meta:
        model = TicketOption
        fields = "__all__"
        read_only_fields = ["price"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        view = kwargs.get("context").get("view")
        if view and hasattr(view, "kwargs"):
            if ticket_pk := view.kwargs["ticket_pk"]:
                try:
                    self.fields[
                        "option"
                    ].queryset = Ticket.objects.get_available_options(ticket_pk)
                except Ticket.DoesNotExist:
                    self.fields["option"].queryset = None


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_field = ["booking", "status", "created_at", "updated_at"]
