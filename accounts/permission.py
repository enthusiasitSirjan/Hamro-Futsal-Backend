from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_role == "OWNER"


class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_role == "USER"


class IsMine(BasePermission):
    def has_permission(self, request, view, obj):
        return request.user == object.user


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_role == "ADMIN"
