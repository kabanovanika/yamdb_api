from rest_framework import permissions

from users.models import UserRoles


class MyCustomPermissionClass(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            return request.user.is_superuser
        return True


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsAMOrOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
                obj.author == request.user or
                request.method in permissions.SAFE_METHODS or
                request.user.role == UserRoles.MODERATOR or
                request.user.role == UserRoles.ADMIN
        )


class RetrieveUpdateDestroyPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if (request.method in ['PUT', 'PATCH', 'DELETE'] and
                request.user.is_authenticated):
            return (
                    obj.author == request.user or
                    request.user.role == UserRoles.ADMIN or
                    request.user.role == UserRoles.MODERATOR
            )
        elif request.method in ['GET']:
            return True


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                view.action in ['update', 'partial_update', 'destroy',
                                'create', ] and
                request.user.role == UserRoles.ADMIN)


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                view.action in ['update', 'partial_update', 'destroy',
                                'create', ] and
                request.user.role == UserRoles.MODERATOR)


class IsAnon(permissions.BasePermission):
    def has_permission(self, request, view):
        return (not request.user.is_authenticated and
                view.action in ['list', 'retrieve'])


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return True
        if user.is_authenticated:
            return bool(user.is_staff or user.role == UserRoles.ADMIN)
