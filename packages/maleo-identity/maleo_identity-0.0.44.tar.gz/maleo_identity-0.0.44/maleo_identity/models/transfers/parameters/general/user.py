from __future__ import annotations
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_metadata.models.expanded_schemas.user_type import MaleoMetadataUserTypeExpandedSchemas
from maleo_identity.models.schemas.user import MaleoIdentityUserSchemas

class MaleoIdentityUserGeneralParametersTransfers:
    class GetSingleQuery(
        MaleoIdentityUserSchemas.Expand,
        BaseParameterSchemas.OptionalListOfStatuses
    ): pass

    class BaseGetSingle(
        BaseParameterSchemas.IdentifierValue,
        MaleoIdentityUserSchemas.IdentifierType
    ): pass

    class GetSinglePassword(BaseGetSingle): pass

    class GetSingle(
        MaleoIdentityUserSchemas.Expand,
        BaseParameterSchemas.OptionalListOfStatuses,
        BaseGetSingle
    ): pass

    class CreateOrUpdateQuery(MaleoIdentityUserSchemas.Expand): pass

    class UpdateData(
        MaleoIdentityUserSchemas.Phone,
        MaleoIdentityUserSchemas.Email,
        MaleoIdentityUserSchemas.Username,
        MaleoMetadataUserTypeExpandedSchemas.SimpleUserType
    ): pass

    class CreateData(
        MaleoIdentityUserSchemas.Password,
        UpdateData,
        MaleoIdentityUserSchemas.OptionalOrganizationId
    ): pass

    class Update(
        CreateOrUpdateQuery,
        UpdateData,
        BaseParameterSchemas.IdentifierValue,
        MaleoIdentityUserSchemas.IdentifierType
    ): pass

    class Create(
        CreateOrUpdateQuery,
        CreateData
    ): pass