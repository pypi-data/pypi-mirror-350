from __future__ import annotations
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_identity.models.schemas.general import MaleoIdentityGeneralSchemas
from maleo_identity.models.schemas.user_organization_role import MaleoIdentityUserOrganizationRoleSchemas

class MaleoIdentityUserOrganizationRoleGeneralParametersTransfers:
    class GetSingleQuery(
        MaleoIdentityUserOrganizationRoleSchemas.Expand,
        BaseParameterSchemas.OptionalListOfStatuses
    ): pass

    class GetSingle(
        MaleoIdentityUserOrganizationRoleSchemas.Expand,
        BaseParameterSchemas.OptionalListOfStatuses,
        MaleoIdentityUserOrganizationRoleSchemas.Key,
        MaleoIdentityGeneralSchemas.OrganizationId,
        MaleoIdentityGeneralSchemas.UserId
    ): pass