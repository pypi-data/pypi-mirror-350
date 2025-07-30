from pydantic import Field
from maleo_foundation.models.responses import BaseResponses
from maleo_identity.enums.user import MaleoIdentityUserEnums
from maleo_identity.models.transfers.general.user import UserTransfers, PasswordTransfers

class MaleoIdentityUserResponses:
    class InvalidIdentifierType(BaseResponses.BadRequest):
        code:str = "IDT-USR-001"
        message:str = "Invalid identifier type"
        description:str = "Invalid identifier type is given in the request"
        other: str = f"Valid identifier types: {[f'{e.name} ({e.value})' for e in MaleoIdentityUserEnums.IdentifierType]}"

    class InvalidValueType(BaseResponses.BadRequest):
        code:str = "IDT-USR-002"
        message:str = "Invalid value type"
        description:str = "Invalid value type is given in the request"

    class GetSingle(BaseResponses.SingleData):
        code:str = "IDT-USR-003"
        message:str = "User found"
        description:str = "Requested user found in database"
        data:UserTransfers = Field(..., description="User")

    class GetMultiple(BaseResponses.PaginatedMultipleData):
        code:str = "IDT-USR-004"
        message:str = "Users found"
        description:str = "Requested users found in database"
        data:list[UserTransfers] = Field(..., description="Users")

    class CreateFailed(BaseResponses.BadRequest):
        code:str = "IDT-USR-005"
        message:str = "Failed creating new user"

    class CreateSuccess(BaseResponses.SingleData):
        code:str = "IDT-USR-006"
        message:str = "Successfully created new user"
        data:UserTransfers = Field(..., description="User")

    class UpdateFailed(BaseResponses.BadRequest):
        code:str = "IDT-USR-007"
        message:str = "Failed updating user's data"

    class UpdateSuccess(BaseResponses.SingleData):
        code:str = "IDT-USR-008"
        message:str = "Successfully updated user's data"
        data:UserTransfers = Field(..., description="User")

    class GetSinglePasswordFailed(BaseResponses.BadRequest):
        code:str = "IDT-USR-009"
        message:str = "Failed fetching user's password"

    class GetSinglePasswordSuccess(BaseResponses.SingleData):
        code:str = "IDT-USR-010"
        message:str = "User's password found"
        description:str = "Requested user's password found in database"
        data:PasswordTransfers = Field(..., description="User's password")