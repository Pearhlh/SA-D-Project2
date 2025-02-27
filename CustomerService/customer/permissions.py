from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.role == "admin":
            return True
        if request.method in SAFE_METHODS and not getattr(view, 'kwargs', {}).get('pk'):
            return False

        return True

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.role == "admin":
            return True
        return obj.id == request.user.id
