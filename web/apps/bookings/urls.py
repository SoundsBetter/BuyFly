from django.urls import path
from .views import PayView

urlpatterns = [
    path('bookings/<int:booking_id>/pay/', PayView.as_view(), name='pay_view'),
]

