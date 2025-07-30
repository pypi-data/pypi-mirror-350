from __future__ import annotations
from .organization import OrganizationsTable
from .organization_role import OrganizationRolesTable
from .user import UsersTable
from .user_profile import UserProfilesTable
from .user_system_role import UserSystemRolesTable
from .user_organization import UserOrganizationsTable
from .user_organization_role import UserOrganizationRolesTable

class MaleoIdentityTables:
    Organization = OrganizationsTable
    OrganizationRole = OrganizationRolesTable
    User = UsersTable
    UserProfile = UserProfilesTable
    UserSystemRole = UserSystemRolesTable
    UserOrganization = UserOrganizationsTable
    UserOrganizationRole = UserOrganizationRolesTable