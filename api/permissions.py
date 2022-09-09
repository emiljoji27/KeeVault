from cgi import print_directory
from rest_framework import permissions

class IsStaffEditorPermission(permissions.DjangoModelPermissions):

    def has_permission(self, request, view):
        print(request.user)
        if not request.user.is_authenticated:
            return False
        return super().has_permission(request, view)
