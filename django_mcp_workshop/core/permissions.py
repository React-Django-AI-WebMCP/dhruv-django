"""
Base permission classes for API views. Extend for role-based or object-level checks.
"""
from rest_framework import permissions


class IsAuthenticatedReadOnly(permissions.BasePermission):
    """Allow read-only for authenticated users; write for staff/superuser only."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and (
            getattr(request.user, "is_staff", False) or getattr(request.user, "is_superuser", False)
        )
