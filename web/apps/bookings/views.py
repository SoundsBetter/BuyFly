from django.views.generic import TemplateView

from .services import create_payment_for_booking

class PayView(TemplateView):
    template_name = 'billing/pay.html'

    def get_context_data(self, booking_id, **kwargs):
        context = super().get_context_data()
        data, signature = create_payment_for_booking(booking_id=booking_id)
        context["data"] = data
        context['signature'] = signature
        return context
