from __future__ import annotations
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_foundation.models.transfers.parameters.client import BaseClientParametersTransfers
from maleo_metadata.models.expanded_schemas.user_type import MaleoMetadataUserTypeExpandedSchemas
from maleo_metadata.models.expanded_schemas.blood_type import MaleoMetadataBloodTypeExpandedSchemas
from maleo_metadata.models.expanded_schemas.gender import MaleoMetadataGenderExpandedSchemas
from maleo_identity.models.schemas.user import MaleoIdentityUserSchemas

class MaleoIdentityUserClientParametersTransfers:
    class GetMultiple(
        MaleoIdentityUserSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultiple,
        MaleoMetadataBloodTypeExpandedSchemas.OptionalListOfSimpleBloodTypes,
        MaleoMetadataGenderExpandedSchemas.OptionalListOfSimpleGenders,
        MaleoIdentityUserSchemas.OptionalListOfPhones,
        MaleoIdentityUserSchemas.OptionalListOfEmails,
        MaleoIdentityUserSchemas.OptionalListOfUsernames,
        MaleoMetadataUserTypeExpandedSchemas.OptionalListOfSimpleUserTypes,
        BaseParameterSchemas.OptionalListOfUuids,
        BaseParameterSchemas.OptionalListOfIds
    ): pass

    class GetMultipleQuery(
        MaleoIdentityUserSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        MaleoMetadataBloodTypeExpandedSchemas.OptionalListOfSimpleBloodTypes,
        MaleoMetadataGenderExpandedSchemas.OptionalListOfSimpleGenders,
        MaleoIdentityUserSchemas.OptionalListOfPhones,
        MaleoIdentityUserSchemas.OptionalListOfEmails,
        MaleoIdentityUserSchemas.OptionalListOfUsernames,
        MaleoMetadataUserTypeExpandedSchemas.OptionalListOfSimpleUserTypes,
        BaseParameterSchemas.OptionalListOfUuids,
        BaseParameterSchemas.OptionalListOfIds
    ): pass