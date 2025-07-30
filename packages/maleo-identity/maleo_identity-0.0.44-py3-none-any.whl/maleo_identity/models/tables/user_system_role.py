from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum, Integer
from maleo_metadata.enums.system_role import MaleoMetadataSystemRoleEnums
from maleo_identity.db import MaleoIdentityMetadataManager

class UserSystemRolesTable(MaleoIdentityMetadataManager.Base):
    __tablename__ = "user_system_roles"
    #* Foreign Key and Relationship to UsersTable
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    user_details = relationship("UsersTable", back_populates="system_roles")
    system_role = Column(
        name="system_role",
        type_=Enum(MaleoMetadataSystemRoleEnums.SystemRole, name="system_role"),
        default=MaleoMetadataSystemRoleEnums.SystemRole.USER,
        nullable=False
    )