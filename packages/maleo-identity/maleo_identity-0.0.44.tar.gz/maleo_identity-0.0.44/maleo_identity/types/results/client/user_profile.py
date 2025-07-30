from typing import Union
from maleo_identity.models.transfers.results.client.user_profile import MaleoIdentityUserProfileClientResultsTransfers

class MaleoIdentityUserProfileClientResultsTypes:
    GetMultiple = Union[
        MaleoIdentityUserProfileClientResultsTransfers.Fail,
        MaleoIdentityUserProfileClientResultsTransfers.NoData,
        MaleoIdentityUserProfileClientResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityUserProfileClientResultsTransfers.Fail,
        MaleoIdentityUserProfileClientResultsTransfers.SingleData
    ]

    CreateOrUpdate = Union[
        MaleoIdentityUserProfileClientResultsTransfers.Fail,
        MaleoIdentityUserProfileClientResultsTransfers.SingleData
    ]