from __future__ import annotations
from .general import MaleoIdentityGeneralEnums
from .organization_role import MaleoIdentityOrganizationRoleEnums
from .organization import MaleoIdentityOrganizationEnums
from .user_organization_role import MaleoIdentityUserOrganizationRoleEnums
from .user_organization import MaleoIdentityUserOrganizationEnums
from .user_profile import MaleoIdentityUserProfileEnums
from .user_system_role import MaleoIdentityUserSystemRoleEnums
from .user import MaleoIdentityUserEnums

class MaleoIdentityEnums:
    General = MaleoIdentityGeneralEnums
    OrganizationRole = MaleoIdentityOrganizationRoleEnums
    Organization = MaleoIdentityOrganizationEnums
    UserOrganizationRole = MaleoIdentityOrganizationRoleEnums
    UserOrganization = MaleoIdentityUserOrganizationEnums
    UserProfile = MaleoIdentityUserProfileEnums
    UserSystemRole = MaleoIdentityUserSystemRoleEnums
    User = MaleoIdentityUserEnums