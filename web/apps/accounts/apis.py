from rest_framework import viewsets, permissions

from .models import CheckInManager, GateManager
from .serializers import (
    CheckInManagerSerializer,
    GateManagerSerializer,
)
from .permissions import IsSupervisor


class CheckInManagerViewSet(viewsets.ModelViewSet):
    queryset = CheckInManager.objects.all()
    serializer_class = CheckInManagerSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsSupervisor,
    ]


class GateManagerViewSet(viewsets.ModelViewSet):
    queryset = GateManager.objects.all()
    serializer_class = GateManagerSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsSupervisor,
    ]
