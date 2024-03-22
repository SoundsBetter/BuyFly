from django.contrib import messages
from django.shortcuts import redirect

from .conf import NOT_HAVE_ACCESS


class DRFPermissionCheckMixin:
    permission_classes = []

    def get_permission_object(self):
        return None

    def check_permissions(self, request):
        for permission in [perm() for perm in self.permission_classes]:
            if hasattr(
                    permission, "has_permission"
            ) and not permission.has_permission(request, self):
                messages.error(request, NOT_HAVE_ACCESS)
                return redirect(request.META.get("HTTP_REFERER", "home"))

        obj = self.get_permission_object()
        if obj is not None:
            for permission in [
                perm()
                for perm in self.permission_classes
                if hasattr(perm, "has_object_permission")
            ]:
                if not permission.has_object_permission(request, self, obj):
                    messages.error(request, NOT_HAVE_ACCESS)
                    return redirect(request.META.get("HTTP_REFERER", "home"))

    def dispatch(self, request, *args, **kwargs):
        permission_check = self.check_permissions(request)
        if permission_check:
            return permission_check
        return super().dispatch(request, *args, **kwargs)  # type:ignore
