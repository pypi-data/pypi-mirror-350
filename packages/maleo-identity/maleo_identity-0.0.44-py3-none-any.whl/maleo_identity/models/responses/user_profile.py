from pydantic import Field
from maleo_foundation.models.responses import BaseResponses
from maleo_identity.enums.user_profile import MaleoIdentityUserProfileEnums
from maleo_identity.models.transfers.general.user_profile import UserProfileTransfers

class MaleoIdentityUserProfileResponses:
    class InvalidIdentifierType(BaseResponses.BadRequest):
        code:str = "IDT-UPR-001"
        message:str = "Invalid identifier type"
        description:str = "Invalid identifier type is given in the request"
        other: str = f"Valid identifier types: {[f'{e.name} ({e.value})' for e in MaleoIdentityUserProfileEnums.IdentifierType]}"

    class InvalidValueType(BaseResponses.BadRequest):
        code:str = "IDT-UPR-002"
        message:str = "Invalid value type"
        description:str = "Invalid value type is given in the request"

    class GetSingle(BaseResponses.SingleData):
        code:str = "IDT-UPR-003"
        message:str = "User profile found"
        description:str = "Requested user profile found in database"
        data:UserProfileTransfers = Field(..., description="User profile")

    class GetMultiple(BaseResponses.PaginatedMultipleData):
        code:str = "IDT-UPR-004"
        message:str = "User profiles found"
        description:str = "Requested user profiles found in database"
        data:list[UserProfileTransfers] = Field(..., description="User profiles")

    class CreateFailed(BaseResponses.BadRequest):
        code:str = "IDT-UPR-005"
        message:str = "Failed creating new user profile"

    class CreateSuccess(BaseResponses.SingleData):
        code:str = "IDT-UPR-006"
        message:str = "Successfully created new user profile"
        data:UserProfileTransfers = Field(..., description="User profile")

    class UpdateFailed(BaseResponses.BadRequest):
        code:str = "IDT-UPR-007"
        message:str = "Failed updating user profile's data"

    class UpdateSuccess(BaseResponses.SingleData):
        code:str = "IDT-UPR-008"
        message:str = "Successfully updated user profile's data"
        data:UserProfileTransfers = Field(..., description="User profile")