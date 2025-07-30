from pydantic import Field
from maleo_foundation.models.responses import BaseResponses
from maleo_identity.models.transfers.general.user_organization_role import UserOrganizationRoleTransfers

class MaleoIdentityUserOrganizationRoleResponses:
    class GetSingle(BaseResponses.SingleData):
        code:str = "IDT-UOR-001"
        message:str = "User organization role found"
        description:str = "Requested user organization role found in database"
        data:UserOrganizationRoleTransfers = Field(..., description="User organization role")

    class GetMultiple(BaseResponses.PaginatedMultipleData):
        code:str = "IDT-UOR-002"
        message:str = "User organization roles found"
        description:str = "Requested user organization roles found in database"
        data:list[UserOrganizationRoleTransfers] = Field(..., description="User organization roles")

    class CreateFailed(BaseResponses.BadRequest):
        code:str = "IDT-UOR-003"
        message:str = "Failed creating new user organization role"

    class CreateSuccess(BaseResponses.SingleData):
        code:str = "IDT-UOR-004"
        message:str = "Successfully created new user organization role"
        data:UserOrganizationRoleTransfers = Field(..., description="User organization role")