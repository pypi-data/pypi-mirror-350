from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer
from maleo_identity.db import MaleoIdentityMetadataManager

class UserOrganizationRolesTable(MaleoIdentityMetadataManager.Base):
    __tablename__ = "user_organization_roles"
    #* Foreign Key UserOrganizationsTable
    user_organization_id = Column(Integer, ForeignKey("user_organizations.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    #* Foreign Key OrganizationRolesTable
    organization_role_id = Column(Integer, ForeignKey("organization_roles.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)