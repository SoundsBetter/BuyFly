from django.urls import path
from .views import PayView, TicketDetailView

app_name = 'bookings'

urlpatterns = [
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('bookings/<int:booking_id>/pay/', PayView.as_view(), name='pay_view'),
]

