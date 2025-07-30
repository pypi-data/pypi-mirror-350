from typing import Union
from maleo_identity.models.transfers.results.repository.user import MaleoIdentityUserRepositoryResultsTransfers

class MaleoIdentityUserRepositoryResultsTypes:
    GetMultiple = Union[
        MaleoIdentityUserRepositoryResultsTransfers.Fail,
        MaleoIdentityUserRepositoryResultsTransfers.NoData,
        MaleoIdentityUserRepositoryResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityUserRepositoryResultsTransfers.Fail,
        MaleoIdentityUserRepositoryResultsTransfers.NoData,
        MaleoIdentityUserRepositoryResultsTransfers.SingleData
    ]

    CreateOrUpdate = Union[
        MaleoIdentityUserRepositoryResultsTransfers.Fail,
        MaleoIdentityUserRepositoryResultsTransfers.SingleData
    ]

    GetSinglePassword = Union[
        MaleoIdentityUserRepositoryResultsTransfers.Fail,
        MaleoIdentityUserRepositoryResultsTransfers.SinglePassword
    ]