from rest_framework import serializers

from .models import Flight, Route, Airport, Seat, Airplane


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'


class RouteSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    departure_airport = serializers.SlugRelatedField(
        slug_field="icao",
        queryset=Airport.objects.all(),
    )
    arrival_airport = serializers.SlugRelatedField(
        slug_field="icao",
        queryset=Airport.objects.all(),
    )

    class Meta:
        model = Route
        fields = "__all__"


class FlightSerializer(serializers.HyperlinkedModelSerializer):
    route = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all())
    arrival_datetime = serializers.SerializerMethodField()
    route_data = RouteSerializer(read_only=True, source="route")

    class Meta:
        model = Flight
        fields = "__all__"
        read_only_fields = ["number"]

    def get_arrival_datetime(self, obj):
        return obj.departure_datetime + obj.duration


class SeatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Seat
        fields = "__all__"


class AirplaneSerializer(serializers.HyperlinkedModelSerializer):
    type = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Airplane
        fields = "__all__"
