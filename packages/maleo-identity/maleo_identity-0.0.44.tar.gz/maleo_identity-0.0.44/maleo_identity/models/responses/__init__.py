from __future__ import annotations
from .organization_role import MaleoIdentityOrganizationRoleResponses
from .organization import MaleoIdentityOrganizationResponses
from .user_organization_role import MaleoIdentityUserOrganizationRoleResponses
from .user_organization import MaleoIdentityUserOrganizationResponses
from .user_profile import MaleoIdentityUserProfileResponses
from .user_system_role import MaleoIdentityUserSystemRoleResponses
from .user import MaleoIdentityUserResponses

class MaleoIdentityResponses:
    OrganizationRole = MaleoIdentityOrganizationRoleResponses
    Organization = MaleoIdentityOrganizationResponses
    UserOrganizationRole = MaleoIdentityUserOrganizationRoleResponses
    UserOrganization = MaleoIdentityUserOrganizationResponses
    UserProfile = MaleoIdentityUserProfileResponses
    UserSystemRole = MaleoIdentityUserSystemRoleResponses
    User = MaleoIdentityUserResponses