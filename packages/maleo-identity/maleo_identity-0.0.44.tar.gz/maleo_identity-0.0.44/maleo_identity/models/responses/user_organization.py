from pydantic import Field
from maleo_foundation.models.responses import BaseResponses
from maleo_identity.models.transfers.general.user_organization import UserOrganizationTransfers

class MaleoIdentityUserOrganizationResponses:
    class GetSingle(BaseResponses.SingleData):
        code:str = "IDT-UOG-001"
        message:str = "User organization found"
        description:str = "Requested user organization found in database"
        data:UserOrganizationTransfers = Field(..., description="User organization")

    class GetMultiple(BaseResponses.PaginatedMultipleData):
        code:str = "IDT-UOG-002"
        message:str = "User organizations found"
        description:str = "Requested user organizations found in database"
        data:list[UserOrganizationTransfers] = Field(..., description="User organizations")

    class AssignFailed(BaseResponses.BadRequest):
        code:str = "IDT-UOG-003"
        message:str = "Failed assigning new user organization"

    class AssignSuccess(BaseResponses.SingleData):
        code:str = "IDT-UOG-004"
        message:str = "Successfully assigned new user organization"
        data:UserOrganizationTransfers = Field(..., description="User organization")