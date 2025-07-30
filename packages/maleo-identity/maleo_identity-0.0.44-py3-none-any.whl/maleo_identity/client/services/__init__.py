from __future__ import annotations
from pydantic import Field
from maleo_foundation.managers.client.base import ClientServices
from maleo_identity.client.services.organization \
    import MaleoIdentityOrganizationClientService
from maleo_identity.client.services.user \
    import MaleoIdentityUserClientService

class MaleoIdentityServices(ClientServices):
    organization:MaleoIdentityOrganizationClientService = Field(..., description="Organization's service")
    user:MaleoIdentityUserClientService = Field(..., description="User's service")