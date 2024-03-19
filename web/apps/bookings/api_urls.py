from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .apis import (
    BookingViewSet,
    PassengerViewSet,
    TicketViewSet,
    OptionViewSet,
    TicketOptionViewSet,
    PaymentViewSet,
    LiqPayCallbackAPIView,
)

router = DefaultRouter()

router.register(r"payments", PaymentViewSet, basename="payments")
router.register(r"options", OptionViewSet, basename="option")
router.register(r"passengers", PassengerViewSet, basename="passenger")
router.register(r"tickets", TicketViewSet, basename="ticket")
router.register(r"", BookingViewSet, basename="booking")

ticket_options_router = NestedSimpleRouter(
    router, r"tickets", lookup="ticket"
)
ticket_options_router.register(
    r"options", TicketOptionViewSet, basename="ticketoption"
)

urlpatterns = [
    path("pay-callback/", LiqPayCallbackAPIView.as_view(), name="pay-callback"),
    path("", include(router.urls)),
    path("", include(ticket_options_router.urls)),

]
