from django.urls import path
from .views import PayView, TicketDetailView, TicketListView

app_name = 'bookings'

urlpatterns = [
    path('tickets/', TicketListView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('bookings/<int:booking_id>/pay/', PayView.as_view(), name='pay_view'),
]
