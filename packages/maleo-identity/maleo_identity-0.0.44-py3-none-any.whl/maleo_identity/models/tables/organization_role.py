from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, Boolean
from maleo_identity.db import MaleoIdentityMetadataManager

class OrganizationRolesTable(MaleoIdentityMetadataManager.Base):
    __tablename__ = "organization_roles"
    #* Foreign Key OrganizationsTable
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    is_default = Column(name="is_default", type_=Boolean, nullable=False, default=False)
    order = Column(name="order", type_=Integer)
    key = Column(name="key", type_=String(50), nullable=False)
    name = Column(name="name", type_=String(50), nullable=False)