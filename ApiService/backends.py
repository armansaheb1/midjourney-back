from rest_framework_simple_api_key.backends import APIKeyAuthentication
from ApiService.models import OrganizationAPIKey


class OrganizationAPIKeyAuthentication(APIKeyAuthentication):
    model = OrganizationAPIKey