from __future__ import annotations
from maleo_foundation.models.transfers.parameters.service import BaseServiceParametersTransfers
from maleo_metadata.models.expanded_schemas.blood_type import MaleoMetadataBloodTypeExpandedSchemas
from maleo_metadata.models.expanded_schemas.gender import MaleoMetadataGenderExpandedSchemas
from maleo_identity.models.schemas.general import MaleoIdentityGeneralSchemas
from maleo_identity.models.schemas.user_profile import MaleoIdentityUserProfileSchemas

class MaleoIdentityUserProfileServiceParametersTransfers:
    class GetMultipleQuery(
        MaleoIdentityUserProfileSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultipleQuery,
        MaleoMetadataBloodTypeExpandedSchemas.OptionalListOfSimpleBloodTypes,
        MaleoMetadataGenderExpandedSchemas.OptionalListOfSimpleGenders,
        MaleoIdentityGeneralSchemas.OptionalListOfUserIds
    ): pass

    class GetMultiple(
        MaleoIdentityUserProfileSchemas.Expand,
        BaseServiceParametersTransfers.GetPaginatedMultiple,
        MaleoMetadataBloodTypeExpandedSchemas.OptionalListOfSimpleBloodTypes,
        MaleoMetadataGenderExpandedSchemas.OptionalListOfSimpleGenders,
        MaleoIdentityGeneralSchemas.OptionalListOfUserIds
    ): pass