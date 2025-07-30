from __future__ import annotations
from maleo_foundation.models.transfers.parameters.service import BaseServiceParametersTransfers
from maleo_metadata.models.expanded_schemas.system_role import MaleoMetadataSystemRoleExpandedSchemas
from maleo_identity.models.schemas.general import MaleoIdentityGeneralSchemas
from maleo_identity.models.schemas.user_system_role import MaleoIdentityUserSystemRoleSchemas

class MaleoIdentityUserSystemRoleServiceParametersTransfers:
    class GetMultipleFromUserQuery(
        MaleoIdentityUserSystemRoleSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        MaleoMetadataSystemRoleExpandedSchemas.OptionalListOfSimpleSystemRoles
    ): pass

    class GetMultipleQuery(
        MaleoIdentityUserSystemRoleSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        MaleoMetadataSystemRoleExpandedSchemas.OptionalListOfSimpleSystemRoles,
        MaleoIdentityGeneralSchemas.OptionalListOfUserIds
    ): pass

    class GetMultiple(
        MaleoIdentityUserSystemRoleSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultiple,
        MaleoMetadataSystemRoleExpandedSchemas.OptionalListOfSimpleSystemRoles,
        MaleoIdentityGeneralSchemas.OptionalListOfUserIds
    ): pass