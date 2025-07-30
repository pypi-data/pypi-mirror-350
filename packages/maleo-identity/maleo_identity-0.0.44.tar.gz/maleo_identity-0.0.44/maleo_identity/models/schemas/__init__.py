from __future__ import annotations
from .general import MaleoIdentityGeneralSchemas
from .organization_role import MaleoIdentityOrganizationRoleSchemas
from .organization import MaleoIdentityOrganizationSchemas
from .user_organization_role import MaleoIdentityUserOrganizationRoleSchemas
from .user_organization import MaleoIdentityUserOrganizationSchemas
from .user_profile import MaleoIdentityUserProfileSchemas
from .user_system_role import MaleoIdentityUserSystemRoleSchemas
from .user import MaleoIdentityUserSchemas

class MaleoIdentitySchemas:
    General = MaleoIdentityGeneralSchemas
    OrganizationRole = MaleoIdentityOrganizationRoleSchemas
    Organization = MaleoIdentityOrganizationSchemas
    UserOrganizationRole = MaleoIdentityUserOrganizationRoleSchemas
    UserOrganization = MaleoIdentityUserOrganizationSchemas
    UserProfile = MaleoIdentityUserProfileSchemas
    UserSystemRole = MaleoIdentityUserSystemRoleSchemas
    User = MaleoIdentityUserSchemas