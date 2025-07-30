from typing import Union
from maleo_identity.models.transfers.results.client.user_system_role import MaleoIdentityUserSystemRoleClientResultsTransfers

class MaleoIdentityUserSystemRoleClientResultsTypes:
    GetMultiple = Union[
        MaleoIdentityUserSystemRoleClientResultsTransfers.Fail,
        MaleoIdentityUserSystemRoleClientResultsTransfers.NoData,
        MaleoIdentityUserSystemRoleClientResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityUserSystemRoleClientResultsTransfers.Fail,
        MaleoIdentityUserSystemRoleClientResultsTransfers.SingleData
    ]

    Assign = Union[
        MaleoIdentityUserSystemRoleClientResultsTransfers.Fail,
        MaleoIdentityUserSystemRoleClientResultsTransfers.SingleData
    ]