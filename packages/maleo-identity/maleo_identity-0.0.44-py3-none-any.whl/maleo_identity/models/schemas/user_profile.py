from pydantic import BaseModel, Field
from typing import List, Optional
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_foundation.types import BaseTypes
from maleo_identity.enums.user_profile import MaleoIdentityUserProfileEnums

class MaleoIdentityUserProfileSchemas:
    class IdentifierType(BaseParameterSchemas.IdentifierType):
        identifier:MaleoIdentityUserProfileEnums.IdentifierType = Field(..., description="User profile's identifier")

    class Expand(BaseParameterSchemas.Expand):
        expand:Optional[List[MaleoIdentityUserProfileEnums.ExpandableFields]] = Field(None, description="Expanded field(s)")

    class IdCard(BaseModel):
        id_card:str = Field(..., max_length=16, description="User's ID Card")

    class LeadingTitle(BaseModel):
        leading_title:BaseTypes.OptionalString = Field(None, max_length=25, description="User's leading title")

    class FirstName(BaseModel):
        first_name:str = Field(..., max_length=50, description="User's first name")

    class MiddleName(BaseModel):
        middle_name:BaseTypes.OptionalString = Field(None, max_length=50, description="User's middle name")

    class LastName(BaseModel):
        last_name:str = Field(..., max_length=50, description="User's last name")

    class EndingTitle(BaseModel):
        ending_title:BaseTypes.OptionalString = Field(None, max_length=25, description="User's ending title")

    class FullName(BaseModel):
        full_name:str = Field(..., max_length=200, description="User's full name")

    class BirthPlace(BaseModel):
        birth_place:BaseTypes.OptionalString = Field(None, max_length=50, description="User's birth place")

    class BirthDate(BaseModel):
        birth_date:BaseTypes.OptionalDate = Field(None, description="User's birth date")