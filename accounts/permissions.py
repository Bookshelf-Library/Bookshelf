from rest_framework.permissions import BasePermission
from rest_framework.views import Request


class CreateUserOrIsColaborator(BasePermission):
    def has_permission(self, request: Request, view):
        return (
            request.method == "POST"
            or request.user
            and request.user.is_authenticated
            and request.user.is_superuser
        )


class IsOwnerOrColaborator(BasePermission):
    def has_permission(self, request: Request, view):
        return (
            request.user
            and str(request.user.id) == view.kwargs["account_id"]
            or request.user
            and request.user.is_superuser
        )
