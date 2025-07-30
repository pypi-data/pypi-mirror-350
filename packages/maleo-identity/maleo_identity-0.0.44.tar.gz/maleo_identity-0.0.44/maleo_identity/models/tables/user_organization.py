from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer
from maleo_identity.db import MaleoIdentityMetadataManager

class UserOrganizationsTable(MaleoIdentityMetadataManager.Base):
    __tablename__ = "user_organizations"
    #* Foreign Key UsersTable
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    #* Foreign Key OrganizationsTable
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)