import secrets

from django.conf import settings
from django.shortcuts import get_object_or_404
from liqpay import LiqPay

from apps.bookings.models import Booking


def create_payment_for_booking(
        booking_id: int,
        public_key: str = settings.LIQPAY_PUBLIC_KEY,
        private_key: str = settings.LIQPAY_PRIVATE_KEY,
        sand_box_mode: int = settings.LIQPAY_SANDBOX_MODE,
        server_url: str = settings.LIQPAY_CALLBACK_URL,

) -> tuple[str, str]:
    booking = get_object_or_404(Booking, id=booking_id)
    liqpay = LiqPay(public_key, private_key)
    params = {
        'action': 'pay',
        'amount': str(booking.price),
        'currency': 'USD',
        'description': f'Payment {booking.number}',
        "order_id": f"{secrets.token_hex(8)}", # temporary use for testing
        # 'order_id': f'{booking.number}'
        'version': '3',
        'sandbox': sand_box_mode,
        'server_url': server_url,
    }
    data = liqpay.cnb_data(params)
    signature = liqpay.cnb_signature(params)
    return data, signature
