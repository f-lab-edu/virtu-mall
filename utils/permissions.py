from typing import Any

from django.http import HttpRequest
from rest_framework import permissions
from rest_framework.views import View

# from apps.user.models import User


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request: HttpRequest, view: View, obj: Any) -> bool:
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        # Write permissions are only allowed to the owner of the obj.
        return obj.user == request.user
