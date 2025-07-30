from __future__ import annotations
from .organization import MaleoIdentityOrganizationConstants
from .organization_role import MaleoIdentityOrganizationRoleConstants
from .user import MaleoIdentityUserConstants
from .user_organization_role import MaleoIdentityUserOrganizationRoleConstants
from .user_organization import MaleoIdentityUserOrganizationConstants
from .user_profile import MaleoIdentityUserProfileConstants
from .user_system_role import MaleoIdentityUserSystemRoleConstants

class MaleoIdentityConstants:
    Organization = MaleoIdentityOrganizationConstants
    OrganizationRole = MaleoIdentityOrganizationRoleConstants
    User = MaleoIdentityUserConstants
    UserOrganizationRole = MaleoIdentityUserOrganizationRoleConstants
    UserOrganization = MaleoIdentityUserOrganizationConstants
    UserProfile = MaleoIdentityUserProfileConstants
    UserSystemRole = MaleoIdentityUserSystemRoleConstants