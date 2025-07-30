from __future__ import annotations
from maleo_foundation.models.transfers.parameters.client import BaseClientParametersTransfers
from maleo_metadata.models.expanded_schemas.system_role import MaleoMetadataSystemRoleExpandedSchemas
from maleo_identity.models.schemas.general import MaleoIdentityGeneralSchemas
from maleo_identity.models.schemas.user_system_role import MaleoIdentityUserSystemRoleSchemas

class MaleoIdentityUserSystemRoleClientParametersTransfers:
    class GetMultipleFromUser(
        MaleoIdentityUserSystemRoleSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultiple,
        MaleoMetadataSystemRoleExpandedSchemas.OptionalListOfSimpleSystemRoles,
        MaleoIdentityGeneralSchemas.UserId
    ): pass
    
    class GetMultiple(
        MaleoIdentityUserSystemRoleSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultiple,
        MaleoMetadataSystemRoleExpandedSchemas.OptionalListOfSimpleSystemRoles,
        MaleoIdentityGeneralSchemas.OptionalListOfUserIds
    ): pass

    class GetMultipleFromUserQuery(
        MaleoIdentityUserSystemRoleSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        MaleoMetadataSystemRoleExpandedSchemas.OptionalListOfSimpleSystemRoles
    ): pass

    class GetMultipleQuery(
        MaleoIdentityUserSystemRoleSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        MaleoMetadataSystemRoleExpandedSchemas.OptionalListOfSimpleSystemRoles,
        MaleoIdentityGeneralSchemas.OptionalListOfUserIds
    ): pass