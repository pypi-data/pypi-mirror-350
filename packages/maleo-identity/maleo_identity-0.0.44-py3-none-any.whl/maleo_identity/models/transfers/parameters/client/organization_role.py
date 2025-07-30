from __future__ import annotations
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_foundation.models.transfers.parameters.client import BaseClientParametersTransfers
from maleo_identity.models.schemas.general import MaleoIdentityGeneralSchemas
from maleo_identity.models.schemas.organization_role import MaleoIdentityOrganizationRoleSchemas

class MaleoIdentityOrganizationRoleClientParametersTransfers:
    class GetMultipleFromOrganization(
        MaleoIdentityOrganizationRoleSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultiple,
        BaseParameterSchemas.OptionalListOfKeys,
        MaleoIdentityGeneralSchemas.OrganizationId
    ): pass
    
    class GetMultiple(
        MaleoIdentityOrganizationRoleSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultiple,
        BaseParameterSchemas.OptionalListOfKeys,
        MaleoIdentityGeneralSchemas.OptionalListOfOrganizationIds
    ): pass

    class GetMultipleFromOrganizationQuery(
        MaleoIdentityOrganizationRoleSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        BaseParameterSchemas.OptionalListOfKeys
    ): pass

    class GetMultipleQuery(
        MaleoIdentityOrganizationRoleSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        BaseParameterSchemas.OptionalListOfKeys,
        MaleoIdentityGeneralSchemas.OptionalListOfOrganizationIds
    ): pass