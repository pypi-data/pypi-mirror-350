from pydantic import Field
from maleo_foundation.models.responses import BaseResponses
from maleo_identity.models.transfers.general.user_system_role import UserSystemRoleTransfers

class MaleoIdentityUserSystemRoleResponses:
    class GetSingle(BaseResponses.SingleData):
        code:str = "IDT-URL-001"
        message:str = "User system role found"
        description:str = "Requested user system role found in database"
        data:UserSystemRoleTransfers = Field(..., description="User system role")

    class GetMultiple(BaseResponses.PaginatedMultipleData):
        code:str = "IDT-URL-002"
        message:str = "User system roles found"
        description:str = "Requested user system roles found in database"
        data:list[UserSystemRoleTransfers] = Field(..., description="User system roles")

    class AssignFailed(BaseResponses.BadRequest):
        code:str = "IDT-URL-003"
        message:str = "Failed assigning new user system role"

    class AssignSuccess(BaseResponses.SingleData):
        code:str = "IDT-URL-004"
        message:str = "Successfully assigned new user system role"
        data:UserSystemRoleTransfers = Field(..., description="User system role")