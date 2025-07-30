from typing import Union
from maleo_identity.models.transfers.results.repository.user_profile import MaleoIdentityUserProfileRepositoryResultsTransfers

class MaleoIdentityUserProfileRepositoryResultsTypes:
    GetMultiple = Union[
        MaleoIdentityUserProfileRepositoryResultsTransfers.Fail,
        MaleoIdentityUserProfileRepositoryResultsTransfers.NoData,
        MaleoIdentityUserProfileRepositoryResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityUserProfileRepositoryResultsTransfers.Fail,
        MaleoIdentityUserProfileRepositoryResultsTransfers.NoData,
        MaleoIdentityUserProfileRepositoryResultsTransfers.SingleData
    ]

    CreateOrUpdate = Union[
        MaleoIdentityUserProfileRepositoryResultsTransfers.Fail,
        MaleoIdentityUserProfileRepositoryResultsTransfers.SingleData
    ]