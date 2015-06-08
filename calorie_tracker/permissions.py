__author__ = 'sameer'

from rest_framework import permissions


class IsOwnerOrStaff(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the person of the meal, or the admin
        return request.user.is_staff or obj.person.user == request.user

class CreateOnlyIfNotAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated():
            return request.method == "POST"
        else:
            return True

class SuperuserOrSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj.user == request.user


