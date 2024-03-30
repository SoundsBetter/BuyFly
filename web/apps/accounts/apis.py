from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CheckInManager, GateManager
from .serializers import (
    CheckInManagerSerializer,
    GateManagerSerializer, GroupSerializer,
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


class GetGroupView(APIView):
    def get(self, request):
        group = request.user.groups.first()
        if group:
            return Response(group.name, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User has no groups'}, status=status.HTTP_404_NOT_FOUND)
