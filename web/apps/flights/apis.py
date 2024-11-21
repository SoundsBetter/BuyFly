import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.accounts.permissions import IsSupervisor
from .models import Flight, Route, Seat, Airplane, Airport
from .serializers import (
    FlightSerializer,
    RouteSerializer,
    SeatSerializer,
    AirplaneSerializer,
    AirportSerializer,
)


class BaseViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, IsSupervisor]
        return [permission() for permission in permission_classes]


class FlightFilter(django_filters.FilterSet):
    departure_airport = django_filters.CharFilter(
        field_name='route__departure_airport__icao', lookup_expr='icontains'
    )
    arrival_airport = django_filters.CharFilter(
        field_name='route__arrival_airport__icao', lookup_expr='icontains'
    )
    departure_date = django_filters.CharFilter(
        field_name='departure_datetime', lookup_expr='date'
    )

    class Meta:
        model = Flight
        fields = ['departure_airport', 'arrival_airport', 'departure_date',]


class FlightViewSet(BaseViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FlightFilter

    def perform_create(self, serializer):
        route = serializer.validated_data["route"]
        number = Flight.objects.create_flight_number(route)
        return serializer.save(number=number)


class RouteViewSet(BaseViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class SeatViewSet(ReadOnlyModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer


class AirplaneViewSet(ReadOnlyModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer


class AirportViewSet(ReadOnlyModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class RouteSearchAPIView(APIView):

    def get(self, request, *args, **kwargs):
        departure_airport_id = request.query_params.get("departure_airport")
        arrival_airport_id = request.query_params.get("arrival_airport")
        if not departure_airport_id or not arrival_airport_id:
            return Response(
                {"error": "Departure and arrival airports must be provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        routes = Route.objects.filter(
            departure_airport_id=departure_airport_id,
            arrival_airport_id=arrival_airport_id,
        )
        serializer = RouteSerializer(routes, many=True,
                                     context={"request": request})
        return Response(serializer.data)
