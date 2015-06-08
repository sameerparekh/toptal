__author__ = 'sameer'

from rest_framework import permissions


class IsOwnerOrStaff(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or staff to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the person of the meal, or the admin
        return request.user.is_staff or obj.person.user == request.user

class CreateOnlyIfNotAuth(permissions.BasePermission):
    """
    If the user hasn't authenticated, we can only create objects
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated():
            return request.method == "POST"
        else:
            return True

class SuperuserOrSelf(permissions.BasePermission):
    """
    Only superuser and self can modify user's settings
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj.user == request.user


