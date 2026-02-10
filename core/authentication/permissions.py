# Imports
from rest_framework.permissions import BasePermission


# Class
class UserPermission(BasePermission):
    """
    Permission class that allows:
    - Public access to registration, login, and token refresh
    - Authenticated access to user and post endpoints
    """

    # Endpoints that allow unauthenticated access
    public_basenames = ['auth-register', 'auth-login', 'auth-refresh']

    # Endpoints that require authentication
    authenticated_basenames = ['user', 'post']


    def has_permission(self, request, view):
        """
        Check if the request has permission to access the view.
        """
        # Allow public endpoints without authentication
        if view.basename in self.public_basenames:
            return True

        # Require authentication for protected endpoints
        if view.basename in self.authenticated_basenames:
            return bool(request.user and request.user.is_authenticated)

        # Deny access to unknown endpoints for security
        return False


    def has_object_permission(self, request, view, obj):
        """
        Check if the request has permission to access the object.
        """
        # Public endpoints don't need object-level permissions
        if view.basename in self.public_basenames:
            return True

        # For authenticated endpoints, require authentication
        if view.basename in self.authenticated_basenames:
            if not (request.user and request.user.is_authenticated):
                return False

            # Allow safe methods (GET, HEAD, OPTIONS) for all authenticated users
            if request.method in ['GET', 'HEAD', 'OPTIONS']:
                return True

            # For write operations (POST, PUT, PATCH, DELETE), check ownership
            # Assuming the object has a 'user' field
            return obj.user == request.user

        # Deny by default
        return False

