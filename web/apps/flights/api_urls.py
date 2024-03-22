from django.urls import include, path
from rest_framework import routers

from .apis import FlightViewSet, RouteViewSet, SeatViewSet, AirplaneViewSet

router = routers.DefaultRouter()
router.register(r"airplanes", AirplaneViewSet, basename="airplane")
router.register(r"seats", SeatViewSet, basename="seat")
router.register(r"routes", RouteViewSet, basename="route")
router.register(r"", FlightViewSet, basename="flight")


urlpatterns = [
    path("", include(router.urls))
]
