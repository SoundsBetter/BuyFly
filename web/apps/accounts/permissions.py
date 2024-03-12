from rest_framework.permissions import BasePermission

from .conf import GROUP_SUPERVISORS, GROUP_GATE_MANAGERS, GROUP_CHECK_IN_MANAGERS

class IsSupervisor(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name=GROUP_SUPERVISORS).exists()

class IsGateManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name=GROUP_GATE_MANAGERS).exists()

class IsCheckInManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name=GROUP_CHECK_IN_MANAGERS).exists()
