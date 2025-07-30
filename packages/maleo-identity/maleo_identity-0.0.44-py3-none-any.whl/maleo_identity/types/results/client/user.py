from typing import Union
from maleo_identity.models.transfers.results.client.user import MaleoIdentityUserClientResultsTransfers

class MaleoIdentityUserClientResultsTypes:
    GetMultiple = Union[
        MaleoIdentityUserClientResultsTransfers.Fail,
        MaleoIdentityUserClientResultsTransfers.NoData,
        MaleoIdentityUserClientResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityUserClientResultsTransfers.Fail,
        MaleoIdentityUserClientResultsTransfers.SingleData
    ]

    CreateOrUpdate = Union[
        MaleoIdentityUserClientResultsTransfers.Fail,
        MaleoIdentityUserClientResultsTransfers.SingleData
    ]

    GetSinglePassword = Union[
        MaleoIdentityUserClientResultsTransfers.Fail,
        MaleoIdentityUserClientResultsTransfers.SinglePassword
    ]