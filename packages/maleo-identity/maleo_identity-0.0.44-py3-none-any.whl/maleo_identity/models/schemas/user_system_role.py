from pydantic import Field
from typing import List, Optional
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_identity.enums.user_system_role import MaleoIdentityUserSystemRoleEnums

class MaleoIdentityUserSystemRoleSchemas:
    class Expand(BaseParameterSchemas.Expand):
        expand:Optional[List[MaleoIdentityUserSystemRoleEnums.ExpandableFields]] = Field(None, description="Expanded field(s)")