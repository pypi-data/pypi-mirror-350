from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_identity.models.schemas.general import MaleoIdentityGeneralSchemas
from maleo_identity.models.transfers.general.organization import OptionalExpandedOrganization
from maleo_identity.models.transfers.general.user import OptionalExpandedUser

class UserOrganizationTransfers(
    OptionalExpandedOrganization,
    MaleoIdentityGeneralSchemas.OrganizationId,
    OptionalExpandedUser,
    MaleoIdentityGeneralSchemas.UserId,
    BaseGeneralSchemas.Status,
    BaseGeneralSchemas.Timestamps,
    BaseGeneralSchemas.Identifiers
): pass