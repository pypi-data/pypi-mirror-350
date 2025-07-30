from pydantic import Field
from maleo_foundation.models.responses import BaseResponses
from maleo_identity.models.transfers.general.organization_role import OrganizationRoleTransfers

class MaleoIdentityOrganizationRoleResponses:
    class GetSingle(BaseResponses.SingleData):
        code:str = "IDT-OGR-001"
        message:str = "Organization role found"
        description:str = "Requested organization role found in database"
        data:OrganizationRoleTransfers = Field(..., description="Organization role")

    class GetMultiple(BaseResponses.PaginatedMultipleData):
        code:str = "IDT-OGR-002"
        message:str = "Organization roles found"
        description:str = "Requested organization roles found in database"
        data:list[OrganizationRoleTransfers] = Field(..., description="Organization roles")

    class CreateFailed(BaseResponses.BadRequest):
        code:str = "IDT-OGR-003"
        message:str = "Failed creating new organization role"

    class CreateSuccess(BaseResponses.SingleData):
        code:str = "IDT-OGR-004"
        message:str = "Successfully created new organization role"
        data:OrganizationRoleTransfers = Field(..., description="Organization role")