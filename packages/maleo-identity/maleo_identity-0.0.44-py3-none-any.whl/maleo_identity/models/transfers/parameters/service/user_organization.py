from __future__ import annotations
from maleo_foundation.models.transfers.parameters.service import BaseServiceParametersTransfers
from maleo_identity.models.schemas.general import MaleoIdentityGeneralSchemas
from maleo_identity.models.schemas.user_organization import MaleoIdentityUserOrganizationSchemas

class MaleoIdentityUserOrganizationServiceParametersTransfers:
    class GetMultipleFromUserQuery(
        MaleoIdentityUserOrganizationSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        MaleoIdentityGeneralSchemas.OptionalListOfOrganizationIds
    ): pass

    class GetMultipleFromOrganizationQuery(
        MaleoIdentityUserOrganizationSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        MaleoIdentityGeneralSchemas.OptionalListOfUserIds
    ): pass

    class GetMultipleQuery(
        MaleoIdentityUserOrganizationSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        MaleoIdentityGeneralSchemas.OptionalListOfOrganizationIds,
        MaleoIdentityGeneralSchemas.OptionalListOfUserIds
    ): pass

    class GetMultiple(
        MaleoIdentityUserOrganizationSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultiple,
        MaleoIdentityGeneralSchemas.OptionalListOfOrganizationIds,
        MaleoIdentityGeneralSchemas.OptionalListOfUserIds
    ): pass