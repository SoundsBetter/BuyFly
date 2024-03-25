from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView, DetailView, ListView
from rest_framework.permissions import IsAuthenticated

from .conf import NOT_HAVE_ACCESS
from .mixins import DRFPermissionCheckMixin
from .models import Ticket
from .services import create_payment_for_booking
from ..accounts.conf import (
    GROUP_SUPERVISORS,
    GROUP_GATE_MANAGERS,
    GROUP_CHECK_IN_MANAGERS,
)
from ..accounts.permissions import (
    IsOwner,
    IsSupervisor,
    IsGateManager,
    IsCheckInManager,
)


class PayView(TemplateView):
    template_name = "booking/pay.html"

    def get_context_data(self, booking_id, **kwargs):
        context = super().get_context_data()
        data, signature = create_payment_for_booking(booking_id=booking_id)
        context["data"] = data
        context["signature"] = signature
        return context


class TicketDetailView(DRFPermissionCheckMixin, DetailView):
    model = Ticket
    template_name = "booking/ticket_detail.html"
    permission_classes = [
        IsAuthenticated,
        IsOwner | IsSupervisor | IsGateManager | IsCheckInManager,
    ]

    def get_permission_object(self):
        return self.get_object()


class TicketListView(ListView):
    model = Ticket
    template_name = "booking/tickets_list.html"
    context_object_name = "tickets"

    def get_queryset(self):
        queryset = super().get_queryset()
        flight_id = self.request.GET.get("flight_id")
        user_id = self.request.GET.get("user_id")
        user = self.request.user

        if flight_id:
            if user.groups.filter(
                name__in=[
                    GROUP_SUPERVISORS,
                    GROUP_GATE_MANAGERS,
                    GROUP_CHECK_IN_MANAGERS,
                ]
            ).exists():
                queryset = queryset.filter(booking__flight__id=flight_id)
            else:
                queryset = queryset.filter(
                    booking__flight__id=flight_id, passenger__user=user
                )
        if user_id:
            if user.groups.filter(name__in=[
                    GROUP_SUPERVISORS,
                    GROUP_GATE_MANAGERS,
                    GROUP_CHECK_IN_MANAGERS,
                ]
            ).exists() or user_id == str(user.id):
                queryset = queryset.filter(passenger__user__id=user_id)
            else:
                queryset = None
        return queryset

    def dispatch(self, *args, **kwargs):
        user_id = self.request.GET.get("user_id")
        user = self.request.user

        if user_id:
            if not user.groups.filter(name__in=[
                GROUP_SUPERVISORS,
                GROUP_GATE_MANAGERS,
                GROUP_CHECK_IN_MANAGERS,
            ]).exists() and user_id != str(user.id):
                messages.error(self.request, NOT_HAVE_ACCESS)
                return redirect("home")

        return super().dispatch(*args, **kwargs)

