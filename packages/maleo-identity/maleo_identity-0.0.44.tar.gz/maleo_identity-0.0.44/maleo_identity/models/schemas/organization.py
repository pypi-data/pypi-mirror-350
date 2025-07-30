from pydantic import BaseModel, Field
from typing import List, Optional
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_foundation.types import BaseTypes
from maleo_identity.enums.organization import MaleoIdentityOrganizationEnums

class MaleoIdentityOrganizationSchemas:
    class IdentifierType(BaseParameterSchemas.IdentifierType):
        identifier:MaleoIdentityOrganizationEnums.IdentifierType = Field(..., description="Organization's identifier")

    class Expand(BaseParameterSchemas.Expand):
        expand:Optional[List[MaleoIdentityOrganizationEnums.ExpandableFields]] = Field(None, description="Expanded field(s)")

    class OptionalParentId(BaseModel):
        parent_id:BaseTypes.OptionalInteger = Field(None, ge=1, description="Parent organization's Id")

    class OptionalListOfParentIds(BaseModel):
        parent_ids:BaseTypes.OptionalListOfIntegers = Field(None, description="Parent organization's Ids")

    class Key(BaseGeneralSchemas.Key):
        key:str = Field(..., max_length=255, description="Organization's key")

    class Name(BaseGeneralSchemas.Name):
        name:str = Field(..., max_length=255, description="Organization's name")