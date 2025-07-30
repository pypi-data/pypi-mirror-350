from __future__ import annotations
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_foundation.models.transfers.parameters.service import BaseServiceParametersTransfers
from maleo_identity.models.schemas.general import MaleoIdentityGeneralSchemas
from maleo_identity.models.schemas.user_organization_role import MaleoIdentityUserOrganizationRoleSchemas

class MaleoIdentityUserOrganizationRoleServiceParametersTransfers:
    class GetMultipleFromUserOrOrganizationQuery(
        MaleoIdentityUserOrganizationRoleSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        BaseParameterSchemas.OptionalListOfKeys
    ): pass

    class GetMultipleQuery(
        MaleoIdentityUserOrganizationRoleSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        BaseParameterSchemas.OptionalListOfKeys,
        MaleoIdentityGeneralSchemas.OptionalListOfOrganizationIds,
        MaleoIdentityGeneralSchemas.OptionalListOfUserIds
    ): pass

    class GetMultiple(
        MaleoIdentityUserOrganizationRoleSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultiple,
        BaseParameterSchemas.OptionalListOfKeys,
        MaleoIdentityGeneralSchemas.OptionalListOfOrganizationIds,
        MaleoIdentityGeneralSchemas.OptionalListOfUserIds
    ): pass