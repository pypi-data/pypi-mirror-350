from __future__ import annotations
from pydantic import Field
from maleo_foundation.managers.client.base import ClientServiceControllers, ClientControllers

from maleo_identity.client.controllers.http.organization \
    import MaleoIdentityOrganizationHTTPController
class MaleoIdentityOrganizationControllers(ClientServiceControllers):
    http:MaleoIdentityOrganizationHTTPController = Field(..., description="Organization's http controller")

from maleo_identity.client.controllers.http.user \
    import MaleoIdentityUserHTTPController
class MaleoIdentityUserControllers(ClientServiceControllers):
    http:MaleoIdentityUserHTTPController = Field(..., description="User's http controller")

class MaleoIdentityControllers(ClientControllers):
    organization:MaleoIdentityOrganizationControllers = Field(..., description="Organization's controllers")
    user:MaleoIdentityUserControllers = Field(..., description="User's controllers")