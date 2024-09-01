from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsModeratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.filter(name='Moderators').exists()

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in ['PUT', 'PATCH']:
            return request.user.groups.filter(name='Moderators').exists()
        return False


class IsOwnerOrModerator(BasePermission):
    """
    Пользователи могут редактировать и удалять только свои объекты.
    Модераторы могут редактировать и удалять любые объекты.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешить безопасные методы (GET, HEAD, OPTIONS) всем
        if request.method in SAFE_METHODS:
            return True

        # Разрешить доступ владельцу объекта или модератору
        return obj.owner == request.user or request.user.groups.filter(name='Moderators').exists()