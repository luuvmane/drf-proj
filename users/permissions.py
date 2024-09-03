from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrModerator(BasePermission):
    """
    Пользователи могут видеть, редактировать и удалять только свои объекты.
    Модераторы могут видеть, редактировать и удалять любые объекты.
    """
    def has_permission(self, request, view):
        # Разрешить безопасные методы (GET, HEAD, OPTIONS) всем
        if request.method in SAFE_METHODS:
            return True

        # Разрешить доступ пользователю или модератору
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Разрешить безопасные методы (GET, HEAD, OPTIONS) всем
        if request.method in SAFE_METHODS:
            return True

        # Разрешить доступ владельцу объекта или модератору
        return obj.owner == request.user or request.user.groups.filter(name='Moderators').exists()
