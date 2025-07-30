from __future__ import annotations
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_foundation.models.transfers.parameters.service import BaseServiceParametersTransfers
from maleo_metadata.models.expanded_schemas.organization_type import MaleoMetadataOrganizationTypeExpandedSchemas
from maleo_identity.models.schemas.organization import MaleoIdentityOrganizationSchemas

class MaleoIdentityOrganizationServiceParametersTransfers:
    class GetMultipleChildrenQuery(
        MaleoIdentityOrganizationSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        BaseParameterSchemas.OptionalListOfKeys,
        BaseGeneralSchemas.IsLeaf,
        BaseGeneralSchemas.IsParent,
        MaleoMetadataOrganizationTypeExpandedSchemas.OptionalListOfSimpleOrganizationTypes,
        BaseParameterSchemas.OptionalListOfUuids,
        BaseParameterSchemas.OptionalListOfIds
    ): pass

    class GetMultipleQuery(
        MaleoIdentityOrganizationSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
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

    class GetMultipleStructuredQuery(
        MaleoIdentityOrganizationSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        BaseParameterSchemas.OptionalListOfKeys,
        MaleoIdentityOrganizationSchemas.OptionalListOfParentIds,
        MaleoMetadataOrganizationTypeExpandedSchemas.OptionalListOfSimpleOrganizationTypes,
        BaseParameterSchemas.OptionalListOfUuids,
        BaseParameterSchemas.OptionalListOfIds
    ): pass

    class GetMultiple(
        MaleoIdentityOrganizationSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultiple,
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

    class GetMultipleStructured(
        MaleoIdentityOrganizationSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultiple,
        BaseParameterSchemas.OptionalListOfKeys,
        MaleoIdentityOrganizationSchemas.OptionalListOfParentIds,
        MaleoMetadataOrganizationTypeExpandedSchemas.OptionalListOfSimpleOrganizationTypes,
        BaseParameterSchemas.OptionalListOfUuids,
        BaseParameterSchemas.OptionalListOfIds
    ): pass