from rest_framework import permissions


class IsAccountOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of Account to access it.
    """

    def has_object_permission(self, request, view, obj):
        print("TRIGG")
        return obj.profile.user == request.user
