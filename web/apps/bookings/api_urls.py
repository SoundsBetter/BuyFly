from django.urls import include, path
from rest_framework import routers

from apps.bookings.apis import BookingViewSet

router = routers.DefaultRouter()
router.register(r'', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls))
]