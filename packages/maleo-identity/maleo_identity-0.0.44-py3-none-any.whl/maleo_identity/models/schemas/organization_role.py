from pydantic import Field
from typing import List, Optional
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_identity.enums.organization_role import MaleoIdentityOrganizationRoleEnums

class MaleoIdentityOrganizationRoleSchemas:
    class Expand(BaseParameterSchemas.Expand):
        expand:Optional[List[MaleoIdentityOrganizationRoleEnums.ExpandableFields]] = Field(None, description="Expanded field(s)")

    class Key(BaseGeneralSchemas.Key):
        key:str = Field(..., max_length=50, description="Organization Role's key")

    class Name(BaseGeneralSchemas.Name):
        name:str = Field(..., max_length=50, description="Organization Role's name")