from rest_framework import permissions
from jwt_auth.serializers import *


class IsAuthenticated(permissions.BasePermission):
    message = 'You are not allowed.'


    def has_permission(self, request, view):
        try:
            if request.user.is_active and request.user.is_allowed:
                return True
            else:
                return False
        except:
            return False
class IsSuper(IsAuthenticated):
    message = 'You are not allowed.'


    def has_permission(self, request, view):

        try:
            if request.user.permission == "super":
                return True
            else:
                return False
        except:
            return False
        
class IsOwner(IsAuthenticated):
    message = 'You are not allowed.'


    def has_permission(self, request, view):
        try:
            if request.user.permission == "owner":
                return True
            else:
                return False
        except:
            return False
        
class IsAdmin(IsAuthenticated):
    message = 'You are not allowed.'


    def has_permission(self, request, view):
        try:
            if request.user.permission == "admin":
                return True
            else:
                return False
        except:
            return False