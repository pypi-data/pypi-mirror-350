from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String, Enum, UUID
from uuid import uuid4
from maleo_metadata.enums.organization_type import MaleoMetadataOrganizationTypeEnums
from maleo_identity.db import MaleoIdentityMetadataManager

class OrganizationsTable(MaleoIdentityMetadataManager.Base):
    __tablename__ = "organizations"
    organization_type = Column(
        name="organization_type",
        type_=Enum(MaleoMetadataOrganizationTypeEnums.OrganizationType, name="organization_type"),
        default=MaleoMetadataOrganizationTypeEnums.OrganizationType.REGULAR,
        nullable=False
    )
    parent_id = Column("parent_id", Integer, ForeignKey("organizations.id", ondelete="SET NULL", onupdate="CASCADE"))
    key = Column(name="key", type_=String(255), unique=True, nullable=False)
    name = Column(name="name", type_=String(255), nullable=False)
    secret = Column(name="secret", type_=UUID, default=uuid4, unique=True, nullable=False)
    parent = relationship(
        "OrganizationsTable",
        remote_side="OrganizationsTable.id",
        back_populates="children"
    )
    children = relationship(
        "OrganizationsTable",
        back_populates="parent",
        cascade="all",
        lazy="select",
        foreign_keys="[OrganizationsTable.parent_id]",
        order_by="OrganizationsTable.id"
    )