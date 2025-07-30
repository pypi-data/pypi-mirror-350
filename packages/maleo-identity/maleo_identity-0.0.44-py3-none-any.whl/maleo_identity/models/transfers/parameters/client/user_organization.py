from __future__ import annotations
from maleo_foundation.models.transfers.parameters.client import BaseClientParametersTransfers
from maleo_identity.models.schemas.general import MaleoIdentityGeneralSchemas
from maleo_identity.models.schemas.user_organization import MaleoIdentityUserOrganizationSchemas

class MaleoIdentityUserOrganizationClientParametersTransfers:
    class GetMultipleFromUser(
        MaleoIdentityUserOrganizationSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultiple,
        MaleoIdentityGeneralSchemas.OptionalListOfOrganizationIds,
        MaleoIdentityGeneralSchemas.UserId
    ): pass

    class GetMultipleFromOrganization(
        MaleoIdentityUserOrganizationSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultiple,
        MaleoIdentityGeneralSchemas.OrganizationId,
        MaleoIdentityGeneralSchemas.OptionalListOfUserIds
    ): pass
    
    class GetMultiple(
        MaleoIdentityUserOrganizationSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultiple,
        MaleoIdentityGeneralSchemas.OptionalListOfOrganizationIds,
        MaleoIdentityGeneralSchemas.OptionalListOfUserIds
    ): pass

    class GetMultipleFromUserQuery(
        MaleoIdentityUserOrganizationSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        MaleoIdentityGeneralSchemas.OptionalListOfOrganizationIds
    ): pass

    class GetMultipleFromOrganizationQuery(
        MaleoIdentityUserOrganizationSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        MaleoIdentityGeneralSchemas.OptionalListOfUserIds
    ): pass

    class GetMultipleQuery(
        MaleoIdentityUserOrganizationSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        MaleoIdentityGeneralSchemas.OptionalListOfOrganizationIds,
        MaleoIdentityGeneralSchemas.OptionalListOfUserIds
    ): pass