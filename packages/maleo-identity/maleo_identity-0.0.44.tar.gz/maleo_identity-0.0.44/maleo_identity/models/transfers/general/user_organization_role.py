from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_identity.models.schemas.general import MaleoIdentityGeneralSchemas
from maleo_identity.models.schemas.user_organization_role import MaleoIdentityUserOrganizationRoleSchemas
from maleo_identity.models.transfers.general.organization import OptionalExpandedOrganization
from maleo_identity.models.transfers.general.user import OptionalExpandedUser

class UserOrganizationRoleTransfers(
    MaleoIdentityUserOrganizationRoleSchemas.Name,
    MaleoIdentityUserOrganizationRoleSchemas.Key,
    BaseGeneralSchemas.Order,
    BaseGeneralSchemas.IsDefault,
    OptionalExpandedOrganization,
    MaleoIdentityGeneralSchemas.OrganizationId,
    OptionalExpandedUser,
    MaleoIdentityGeneralSchemas.UserId,
    BaseGeneralSchemas.Status,
    BaseGeneralSchemas.Timestamps,
    BaseGeneralSchemas.Identifiers
): pass