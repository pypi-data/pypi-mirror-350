from pydantic import BaseModel, Field
from typing import Optional
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_metadata.models.expanded_schemas.blood_type import MaleoMetadataBloodTypeExpandedSchemas
from maleo_metadata.models.expanded_schemas.gender import MaleoMetadataGenderExpandedSchemas
from maleo_identity.models.schemas.general import MaleoIdentityGeneralSchemas
from maleo_identity.models.schemas.user_profile import MaleoIdentityUserProfileSchemas

class UserProfileTransfers(
    MaleoMetadataBloodTypeExpandedSchemas.OptionalExpandedBloodType,
    MaleoMetadataBloodTypeExpandedSchemas.OptionalSimpleBloodType,
    MaleoMetadataGenderExpandedSchemas.OptionalExpandedGender,
    MaleoMetadataGenderExpandedSchemas.OptionalSimpleGender,
    MaleoIdentityUserProfileSchemas.BirthDate,
    MaleoIdentityUserProfileSchemas.BirthPlace,
    MaleoIdentityUserProfileSchemas.FullName,
    MaleoIdentityUserProfileSchemas.EndingTitle,
    MaleoIdentityUserProfileSchemas.LastName,
    MaleoIdentityUserProfileSchemas.MiddleName,
    MaleoIdentityUserProfileSchemas.FirstName,
    MaleoIdentityUserProfileSchemas.LeadingTitle,
    MaleoIdentityUserProfileSchemas.IdCard,
    MaleoIdentityGeneralSchemas.UserId,
    BaseGeneralSchemas.Status,
    BaseGeneralSchemas.Timestamps,
    BaseGeneralSchemas.Identifiers
): pass

class OptionalExpandedUserProfile(BaseModel):
    profile:Optional[UserProfileTransfers] = Field(None, description="User's profile")