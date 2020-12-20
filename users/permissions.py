from rest_framework import permissions
from .models import UserRoles


class IsAdminPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated) and \
            request.user.role == UserRoles.ADMIN or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated) and \
            request.user.role == UserRoles.ADMIN or request.user.is_superuser
