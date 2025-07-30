from __future__ import annotations
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_foundation.models.transfers.parameters.client import BaseClientParametersTransfers
from maleo_identity.models.schemas.general import MaleoIdentityGeneralSchemas
from maleo_identity.models.schemas.user_organization_role import MaleoIdentityUserOrganizationRoleSchemas

class MaleoIdentityUserOrganizationRoleClientParametersTransfers:
    class GetMultipleFromUserOrOrganization(
        MaleoIdentityUserOrganizationRoleSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultiple,
        BaseParameterSchemas.OptionalListOfKeys,
        MaleoIdentityGeneralSchemas.OrganizationId,
        MaleoIdentityGeneralSchemas.UserId
    ): pass
    
    class GetMultiple(
        MaleoIdentityUserOrganizationRoleSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultiple,
        BaseParameterSchemas.OptionalListOfKeys,
        MaleoIdentityGeneralSchemas.OptionalListOfOrganizationIds,
        MaleoIdentityGeneralSchemas.OptionalListOfUserIds
    ): pass

    class GetMultipleFromUserOrOrganizationQuery(
        MaleoIdentityUserOrganizationRoleSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        BaseParameterSchemas.OptionalListOfKeys
    ): pass

    class GetMultipleQuery(
        MaleoIdentityUserOrganizationRoleSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        BaseParameterSchemas.OptionalListOfKeys,
        MaleoIdentityGeneralSchemas.OptionalListOfOrganizationIds,
        MaleoIdentityGeneralSchemas.OptionalListOfUserIds
    ): pass