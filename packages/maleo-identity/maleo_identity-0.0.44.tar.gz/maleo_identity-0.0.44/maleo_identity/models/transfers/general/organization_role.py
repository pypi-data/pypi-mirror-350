from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_identity.models.schemas.general import MaleoIdentityGeneralSchemas
from maleo_identity.models.schemas.organization_role import MaleoIdentityOrganizationRoleSchemas
from maleo_identity.models.transfers.general.organization import OptionalExpandedOrganization

class OrganizationRoleTransfers(
    MaleoIdentityOrganizationRoleSchemas.Name,
    MaleoIdentityOrganizationRoleSchemas.Key,
    BaseGeneralSchemas.Order,
    BaseGeneralSchemas.IsDefault,
    OptionalExpandedOrganization,
    MaleoIdentityGeneralSchemas.OrganizationId,
    BaseGeneralSchemas.Status,
    BaseGeneralSchemas.Timestamps,
    BaseGeneralSchemas.Identifiers
): pass