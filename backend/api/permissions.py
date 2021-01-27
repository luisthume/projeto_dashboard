from rest_framework import permissions

class IsSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ["DELETE", "GET", "POST"] and request.user.is_superuser:
                return True
        return False

class IsOwner(permissions.BasePermission):
    message = 'You must be the owner.'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user