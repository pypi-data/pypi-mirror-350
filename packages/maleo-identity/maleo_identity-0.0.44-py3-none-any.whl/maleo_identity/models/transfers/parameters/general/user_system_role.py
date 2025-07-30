from __future__ import annotations
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_metadata.models.expanded_schemas.system_role import MaleoMetadataSystemRoleExpandedSchemas
from maleo_identity.models.schemas.general import MaleoIdentityGeneralSchemas
from maleo_identity.models.schemas.user_system_role import MaleoIdentityUserSystemRoleSchemas

class MaleoIdentityUserSystemRoleGeneralParametersTransfers:
    class GetSingleQuery(
        MaleoIdentityUserSystemRoleSchemas.Expand,
        BaseParameterSchemas.OptionalListOfStatuses
    ): pass

    class GetSingle(
        MaleoIdentityUserSystemRoleSchemas.Expand,
        BaseParameterSchemas.OptionalListOfStatuses,
        MaleoMetadataSystemRoleExpandedSchemas.SimpleSystemRole,
        MaleoIdentityGeneralSchemas.UserId
    ): pass

    class AssignQuery(MaleoIdentityUserSystemRoleSchemas.Expand): pass

    class AssignFromUserBody(MaleoMetadataSystemRoleExpandedSchemas.SimpleSystemRole): pass

    class AssignData(
        MaleoMetadataSystemRoleExpandedSchemas.SimpleSystemRole,
        MaleoIdentityGeneralSchemas.UserId
    ): pass

    class Assign(AssignData, AssignQuery): pass