from __future__ import annotations
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_foundation.models.transfers.parameters.client import BaseClientParametersTransfers
from maleo_metadata.models.expanded_schemas.organization_type import MaleoMetadataOrganizationTypeExpandedSchemas
from maleo_identity.models.schemas.general import MaleoIdentityGeneralSchemas
from maleo_identity.models.schemas.organization import MaleoIdentityOrganizationSchemas

class MaleoIdentityOrganizationClientParametersTransfers:
    class GetMultiple(
        MaleoIdentityOrganizationSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultiple,
        BaseParameterSchemas.OptionalListOfKeys,
        BaseGeneralSchemas.IsLeaf,
        BaseGeneralSchemas.IsChild,
        BaseGeneralSchemas.IsParent,
        BaseGeneralSchemas.IsRoot,
        MaleoIdentityOrganizationSchemas.OptionalListOfParentIds,
        MaleoMetadataOrganizationTypeExpandedSchemas.OptionalListOfSimpleOrganizationTypes,
        BaseParameterSchemas.OptionalListOfUuids,
        BaseParameterSchemas.OptionalListOfIds
    ): pass

    class GetMultipleChildren(
        MaleoIdentityOrganizationSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultiple,
        BaseParameterSchemas.OptionalListOfKeys,
        BaseGeneralSchemas.IsLeaf,
        BaseGeneralSchemas.IsParent,
        MaleoIdentityGeneralSchemas.OrganizationId,
        MaleoMetadataOrganizationTypeExpandedSchemas.OptionalListOfSimpleOrganizationTypes,
        BaseParameterSchemas.OptionalListOfUuids,
        BaseParameterSchemas.OptionalListOfIds
    ): pass

    class GetMultipleStructured(
        BaseClientParametersTransfers.GetPaginatedMultiple,
        BaseParameterSchemas.OptionalListOfKeys,
        MaleoIdentityOrganizationSchemas.OptionalListOfParentIds,
        MaleoMetadataOrganizationTypeExpandedSchemas.OptionalListOfSimpleOrganizationTypes,
        BaseParameterSchemas.OptionalListOfUuids,
        BaseParameterSchemas.OptionalListOfIds
    ): pass

    class GetMultipleQuery(
        MaleoIdentityOrganizationSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        BaseParameterSchemas.OptionalListOfKeys,
        BaseGeneralSchemas.IsLeaf,
        BaseGeneralSchemas.IsChild,
        BaseGeneralSchemas.IsParent,
        BaseGeneralSchemas.IsRoot,
        MaleoIdentityOrganizationSchemas.OptionalListOfParentIds,
        MaleoMetadataOrganizationTypeExpandedSchemas.OptionalListOfSimpleOrganizationTypes,
        BaseParameterSchemas.OptionalListOfUuids,
        BaseParameterSchemas.OptionalListOfIds
    ): pass

    class GetMultipleChildrenQuery(
        MaleoIdentityOrganizationSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        BaseParameterSchemas.OptionalListOfKeys,
        BaseGeneralSchemas.IsLeaf,
        BaseGeneralSchemas.IsParent,
        MaleoMetadataOrganizationTypeExpandedSchemas.OptionalListOfSimpleOrganizationTypes,
        BaseParameterSchemas.OptionalListOfUuids,
        BaseParameterSchemas.OptionalListOfIds
    ): pass

    class GetMultipleStructuredQuery(
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        BaseParameterSchemas.OptionalListOfKeys,
        MaleoIdentityOrganizationSchemas.OptionalListOfParentIds,
        MaleoMetadataOrganizationTypeExpandedSchemas.OptionalListOfSimpleOrganizationTypes,
        BaseParameterSchemas.OptionalListOfUuids,
        BaseParameterSchemas.OptionalListOfIds
    ): pass