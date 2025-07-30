from __future__ import annotations
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_identity.models.schemas.general import MaleoIdentityGeneralSchemas
from maleo_identity.models.schemas.organization_role import MaleoIdentityOrganizationRoleSchemas

class MaleoIdentityOrganizationRoleGeneralParametersTransfers:
    class GetSingleQuery(
        MaleoIdentityOrganizationRoleSchemas.Expand,
        BaseParameterSchemas.OptionalListOfStatuses
    ): pass

    class GetSingle(
        MaleoIdentityOrganizationRoleSchemas.Expand,
        BaseParameterSchemas.OptionalListOfStatuses,
        MaleoIdentityOrganizationRoleSchemas.Key,
        MaleoIdentityGeneralSchemas.OrganizationId
    ): pass