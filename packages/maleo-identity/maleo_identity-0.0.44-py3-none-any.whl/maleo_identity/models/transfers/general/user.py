from pydantic import BaseModel, Field
from typing import Optional
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_metadata.models.expanded_schemas.user_type import MaleoMetadataUserTypeExpandedSchemas
from maleo_identity.models.schemas.user import MaleoIdentityUserSchemas
from maleo_identity.models.transfers.general.user_profile import OptionalExpandedUserProfile

class UserTransfers(
    OptionalExpandedUserProfile,
    MaleoIdentityUserSchemas.Phone,
    MaleoIdentityUserSchemas.Email,
    MaleoIdentityUserSchemas.Username,
    MaleoMetadataUserTypeExpandedSchemas.OptionalExpandedUserType,
    MaleoMetadataUserTypeExpandedSchemas.SimpleUserType,
    BaseGeneralSchemas.Status,
    BaseGeneralSchemas.Timestamps,
    BaseGeneralSchemas.Identifiers
): pass

class OptionalExpandedUser(BaseModel):
    user_details:Optional[UserTransfers] = Field(None, description="User's details")

class PasswordTransfers(MaleoIdentityUserSchemas.Password): pass