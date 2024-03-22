from django.http import Http404
from django.views import View
from django.views.generic import TemplateView, DetailView

from .mixins import UserIsOwnerMixin
from .models import Ticket
from .services import create_payment_for_booking

class PayView(TemplateView):
    template_name = 'booking/pay.html'

    def get_context_data(self, booking_id, **kwargs):
        context = super().get_context_data()
        data, signature = create_payment_for_booking(booking_id=booking_id)
        context["data"] = data
        context['signature'] = signature
        return context


class TicketDetailView(UserIsOwnerMixin, DetailView):
    model = Ticket
    template_name = 'booking/ticket.html'
