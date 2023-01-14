from rest_framework import permissions

# IsAdminUser'ı override ediyoruz.
class IsStafforReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):

        if(request.method in permissions.SAFE_METHODS):
            return True

        return bool(request.user and request.user.is_staff)
