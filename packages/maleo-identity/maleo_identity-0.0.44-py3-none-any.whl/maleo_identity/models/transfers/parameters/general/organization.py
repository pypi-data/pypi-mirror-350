from __future__ import annotations
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_metadata.models.expanded_schemas.organization_type import MaleoMetadataOrganizationTypeExpandedSchemas
from maleo_identity.models.schemas.organization import MaleoIdentityOrganizationSchemas

class MaleoIdentityOrganizationGeneralParametersTransfers:
    class GetSingleQuery(
        MaleoIdentityOrganizationSchemas.Expand,
        BaseParameterSchemas.OptionalListOfStatuses
    ): pass

    class GetSingle(
        MaleoIdentityOrganizationSchemas.Expand,
        BaseParameterSchemas.OptionalListOfStatuses,
        BaseParameterSchemas.IdentifierValue,
        MaleoIdentityOrganizationSchemas.IdentifierType
    ): pass

    class CreateOrUpdateQuery(MaleoIdentityOrganizationSchemas.Expand): pass

    class CreateOrUpdateData(
        MaleoIdentityOrganizationSchemas.Name,
        MaleoIdentityOrganizationSchemas.Key,
        MaleoIdentityOrganizationSchemas.OptionalParentId,
        MaleoMetadataOrganizationTypeExpandedSchemas.SimpleOrganizationType
    ): pass

    class Create(CreateOrUpdateData, CreateOrUpdateQuery): pass

    class Update(
        CreateOrUpdateData,
        CreateOrUpdateQuery,
        BaseParameterSchemas.IdentifierValue,
        MaleoIdentityOrganizationSchemas.IdentifierType
    ): pass