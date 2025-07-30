from __future__ import annotations
from maleo_foundation.models.transfers.parameters.client import BaseClientParametersTransfers
from maleo_metadata.models.expanded_schemas.blood_type import MaleoMetadataBloodTypeExpandedSchemas
from maleo_metadata.models.expanded_schemas.gender import MaleoMetadataGenderExpandedSchemas
from maleo_identity.models.schemas.general import MaleoIdentityGeneralSchemas
from maleo_identity.models.schemas.user_profile import MaleoIdentityUserProfileSchemas

class MaleoIdentityUserProfileClientParametersTransfers:
    class GetMultiple(
        MaleoIdentityUserProfileSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultiple,
        MaleoMetadataBloodTypeExpandedSchemas.OptionalListOfSimpleBloodTypes,
        MaleoMetadataGenderExpandedSchemas.OptionalListOfSimpleGenders,
        MaleoIdentityGeneralSchemas.OptionalListOfUserIds
    ): pass

    class GetMultipleQuery(
        MaleoIdentityUserProfileSchemas.Expand,
        BaseClientParametersTransfers.GetPaginatedMultipleQuery,
        MaleoMetadataBloodTypeExpandedSchemas.OptionalListOfSimpleBloodTypes,
        MaleoMetadataGenderExpandedSchemas.OptionalListOfSimpleGenders,
        MaleoIdentityGeneralSchemas.OptionalListOfUserIds
    ): pass