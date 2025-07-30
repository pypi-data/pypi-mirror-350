from pydantic import Field
from typing import List, Optional
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_identity.enums.user_organization import MaleoIdentityUserOrganizationEnums

class MaleoIdentityUserOrganizationSchemas:
    class Expand(BaseParameterSchemas.Expand):
        expand:Optional[List[MaleoIdentityUserOrganizationEnums.ExpandableFields]] = Field(None, description="Expanded field(s)")