from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_metadata.models.expanded_schemas.system_role import MaleoMetadataSystemRoleExpandedSchemas
from maleo_identity.models.schemas.general import MaleoIdentityGeneralSchemas
from maleo_identity.models.transfers.general.user import OptionalExpandedUser

class UserSystemRoleTransfers(
    MaleoMetadataSystemRoleExpandedSchemas.OptionalExpandedSystemRole,
    MaleoMetadataSystemRoleExpandedSchemas.SimpleSystemRole,
    OptionalExpandedUser,
    MaleoIdentityGeneralSchemas.UserId,
    BaseGeneralSchemas.Status,
    BaseGeneralSchemas.Timestamps,
    BaseGeneralSchemas.Identifiers
): pass