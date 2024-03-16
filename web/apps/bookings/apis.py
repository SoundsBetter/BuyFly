from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .models import Booking
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.groups.filter(name="supervisors").exists():
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        booking = self.get_object()
        if booking.status in ["reserved", "pending"]:
            return super().update(request, *args, **kwargs)
        return Response(
            {"detail": "Booking cannot be updated at this stage."},
            status=status.HTTP_403_FORBIDDEN,
        )

    def destroy(self, request, *args, **kwargs):
        booking = self.get_object()
        if booking.status in ["reserved", "pending"]:
            return super().destroy(request, *args, **kwargs)
        return Response(
            {"detail": "Booking cannot be cancelled at this stage."},
            status=status.HTTP_403_FORBIDDEN,
        )
