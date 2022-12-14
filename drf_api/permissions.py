from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # print('This is Request: ', request)
        # print('This is View: ', view)
        # print('This is Obj: ', obj)
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
