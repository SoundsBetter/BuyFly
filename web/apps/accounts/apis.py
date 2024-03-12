from rest_framework import viewsets, permissions

from apps.accounts.models import CheckInManager, GateManager
from apps.accounts.serializers import (
    CheckInManagerSerializer,
    GateManagerSerializer,
)
from apps.accounts.permissions import IsSupervisor


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
