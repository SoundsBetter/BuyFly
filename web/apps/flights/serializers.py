from rest_framework import serializers

from .models import Flight, Route, Airport


class FlightSerializer(serializers.HyperlinkedModelSerializer):
    route = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all())

    class Meta:
        model = Flight
        fields = '__all__'
        read_only_fields = ['number']


class RouteSerializer(serializers.HyperlinkedModelSerializer):
    departure_airport = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all())
    arrival_airport = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all())
    class Meta:
        model = Route
        fields = '__all__'