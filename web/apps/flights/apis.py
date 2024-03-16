from rest_framework import viewsets, permissions

from apps.accounts.permissions import IsSupervisor
from .models import Flight, Route
from .serializers import FlightSerializer, RouteSerializer


class BaseViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated, IsSupervisor]
        return [permission() for permission in permission_classes]


class FlightViewSet(BaseViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def perform_create(self, serializer):
        route = serializer.validated_data['route']
        number = Flight.objects.create_flight(route)
        return serializer.save(number=number)


class RouteViewSet(BaseViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

