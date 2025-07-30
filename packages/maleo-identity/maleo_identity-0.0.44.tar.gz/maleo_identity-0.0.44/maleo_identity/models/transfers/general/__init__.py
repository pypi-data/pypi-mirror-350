from __future__ import annotations
from .organization import OrganizationTransfers
from .organization_role import OrganizationRoleTransfers
from .user_profile import UserProfileTransfers
from .user import UserTransfers
from .user_system_role import UserSystemRoleTransfers
from .user_organization import UserOrganizationTransfers
from .user_organization_role import UserOrganizationRoleTransfers

class MaleoIdentityGeneralTransfers:
    Organization = OrganizationTransfers
    OrganizationRole = OrganizationRoleTransfers
    UserProfile = UserProfileTransfers
    User = UserTransfers
    UserSystemRole = UserSystemRoleTransfers
    UserOrganization = UserOrganizationTransfers
    UserOrganizationRole = UserOrganizationRoleTransfers