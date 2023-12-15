from typing import Any

from django.http import HttpRequest
from rest_framework import permissions
from rest_framework.views import View

# from apps.user.models import User


class IsAdminOrOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request: HttpRequest, view: View, obj: Any) -> bool:
        is_admin = request.user and request.user.is_staff
        is_owner = obj.user == request.user
        return is_admin or is_owner


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request: HttpRequest, view: View, obj: Any) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
