from typing import Union
from maleo_identity.models.transfers.results.repository.user_system_role import MaleoIdentityUserSystemRoleRepositoryResultsTransfers

class MaleoIdentityUserSystemRoleRepositoryResultsTypes:
    GetMultiple = Union[
        MaleoIdentityUserSystemRoleRepositoryResultsTransfers.Fail,
        MaleoIdentityUserSystemRoleRepositoryResultsTransfers.NoData,
        MaleoIdentityUserSystemRoleRepositoryResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityUserSystemRoleRepositoryResultsTransfers.Fail,
        MaleoIdentityUserSystemRoleRepositoryResultsTransfers.NoData,
        MaleoIdentityUserSystemRoleRepositoryResultsTransfers.SingleData
    ]

    Assign = Union[
        MaleoIdentityUserSystemRoleRepositoryResultsTransfers.Fail,
        MaleoIdentityUserSystemRoleRepositoryResultsTransfers.SingleData
    ]