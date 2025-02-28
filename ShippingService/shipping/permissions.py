import requests
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission, SAFE_METHODS

# url = "http://172.20.0.10:8000/api/auth/verify-token/"
url = "http://host.docker.internal:8000/api/auth/verify-token/"

class VerifyJWT(BasePermission):
    required_roles = []

    def has_permission(self, request, view):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise AuthenticationFailed("No token provided")

        token = auth_header.split("Bearer ")[1]
        response = requests.post(url, headers={"Authorization": f"Bearer {token}"})

        if response.status_code == 200:
            user_data = response.json()
            request.user = user_data
            request.auth = token

            if self.required_roles and user_data.get("role") not in self.required_roles:
                raise AuthenticationFailed("Permission denied")

            return True

        raise AuthenticationFailed("Invalid token")


class IsAdmin(VerifyJWT):
    required_roles = ["admin"]


class IsSeller(VerifyJWT):
    required_roles = ["admin","seller"]

    def has_object_permission(self, request, view, obj):
        if request.user['role'] == 'admin':
            return True
        return obj.owner_id == int(request.user["id"])

class IsBuyer(VerifyJWT):
    required_roles = ["buyer"]

class IsAdminOrBuyer(VerifyJWT):
    required_roles = ["admin","buyer"]


class IsShipper(VerifyJWT):
    required_roles = ["shipper"]