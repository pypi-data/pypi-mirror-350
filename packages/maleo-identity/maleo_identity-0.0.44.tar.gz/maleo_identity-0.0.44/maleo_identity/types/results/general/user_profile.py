from typing import Union
from maleo_identity.models.transfers.results.general.user_profile import MaleoIdentityUserProfileGeneralResultsTransfers

class MaleoIdentityUserProfileGeneralResultsTypes:
    GetMultiple = Union[
        MaleoIdentityUserProfileGeneralResultsTransfers.Fail,
        MaleoIdentityUserProfileGeneralResultsTransfers.NoData,
        MaleoIdentityUserProfileGeneralResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityUserProfileGeneralResultsTransfers.Fail,
        MaleoIdentityUserProfileGeneralResultsTransfers.NoData,
        MaleoIdentityUserProfileGeneralResultsTransfers.SingleData
    ]

    CreateOrUpdate = Union[
        MaleoIdentityUserProfileGeneralResultsTransfers.Fail,
        MaleoIdentityUserProfileGeneralResultsTransfers.SingleData
    ]