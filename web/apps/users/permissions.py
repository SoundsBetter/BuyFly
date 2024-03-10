from rest_framework.permissions import BasePermission


class IsSupervisor(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='supervisors').exists()
