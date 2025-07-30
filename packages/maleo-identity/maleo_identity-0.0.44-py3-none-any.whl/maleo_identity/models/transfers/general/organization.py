from pydantic import BaseModel, Field
from typing import List, Optional
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_metadata.models.expanded_schemas.organization_type import MaleoMetadataOrganizationTypeExpandedSchemas
from maleo_identity.models.schemas.organization import MaleoIdentityOrganizationSchemas

class OrganizationTransfers(
    MaleoIdentityOrganizationSchemas.Name,
    MaleoIdentityOrganizationSchemas.Key,
    MaleoIdentityOrganizationSchemas.OptionalParentId,
    MaleoMetadataOrganizationTypeExpandedSchemas.OptionalExpandedOrganizationType,
    MaleoMetadataOrganizationTypeExpandedSchemas.SimpleOrganizationType,
    BaseGeneralSchemas.Status,
    BaseGeneralSchemas.Timestamps,
    BaseGeneralSchemas.Identifiers
):
    pass

class OptionalExpandedOrganization(BaseModel):
    organization_details:Optional[OrganizationTransfers] = Field(None, description="Organization's details")

class StructuredOrganizationTransfers(OrganizationTransfers):
    children:List["StructuredOrganizationTransfers"] = Field(..., description="Organization children")

# this is required for forward reference resolution
StructuredOrganizationTransfers.model_rebuild()