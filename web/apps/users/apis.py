from rest_framework import viewsets, permissions

from apps.users.models import CheckInManager, User, GateManager
from apps.users.serializers import (
    CheckInManagerSerializer,
    UserSerializer,
    GateManagerSerializer,
)
from apps.users.permissions import IsSupervisor


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]


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
