from __future__ import annotations
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_foundation.models.transfers.parameters.service import BaseServiceParametersTransfers
from maleo_identity.models.schemas.general import MaleoIdentityGeneralSchemas
from maleo_identity.models.schemas.organization_role import MaleoIdentityOrganizationRoleSchemas

class MaleoIdentityOrganizationRoleServiceParametersTransfers:
    class GetMultipleFromOrganizationQuery(
        MaleoIdentityOrganizationRoleSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        BaseParameterSchemas.OptionalListOfKeys
    ): pass

    class GetMultipleQuery(
        MaleoIdentityOrganizationRoleSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        BaseParameterSchemas.OptionalListOfKeys,
        MaleoIdentityGeneralSchemas.OptionalListOfOrganizationIds
    ): pass

    class GetMultiple(
        MaleoIdentityOrganizationRoleSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultiple,
        BaseParameterSchemas.OptionalListOfKeys,
        MaleoIdentityGeneralSchemas.OptionalListOfOrganizationIds
    ): pass