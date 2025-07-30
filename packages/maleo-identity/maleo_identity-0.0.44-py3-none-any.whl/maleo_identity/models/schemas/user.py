from pydantic import BaseModel, Field
from typing import List, Optional
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_foundation.types import BaseTypes
from maleo_identity.enums.user import MaleoIdentityUserEnums

class MaleoIdentityUserSchemas:
    class IdentifierType(BaseParameterSchemas.IdentifierType):
        identifier:MaleoIdentityUserEnums.IdentifierType = Field(..., description="User's identifier")

    class Expand(BaseParameterSchemas.Expand):
        expand:Optional[List[MaleoIdentityUserEnums.ExpandableFields]] = Field(None, description="Expanded field(s)")

    class OptionalOrganizationId(BaseModel):
        organization_id:BaseTypes.OptionalInteger = Field(..., ge=1, description="Organization's ID")

    class Username(BaseModel):
        username:str = Field(..., max_length=50, description="User's username")

    class OptionalListOfUsernames(BaseModel):
        usernames:BaseTypes.OptionalListOfStrings = Field(None, description="Specific usernames")

    class Email(BaseModel):
        email:str = Field(..., max_length=255, description="User's email")

    class OptionalListOfEmails(BaseModel):
        emails:BaseTypes.OptionalListOfStrings = Field(None, description="Specific emails")

    class Phone(BaseModel):
        phone:str = Field(..., max_length=15, description="User's username")

    class OptionalListOfPhones(BaseModel):
        phones:BaseTypes.OptionalListOfStrings = Field(None, description="Specific phones")

    class Password(BaseModel):
        password:str = Field(..., max_length=255, description="User's password")