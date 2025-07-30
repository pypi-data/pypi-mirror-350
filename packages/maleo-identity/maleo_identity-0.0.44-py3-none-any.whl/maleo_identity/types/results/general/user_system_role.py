from typing import Union
from maleo_identity.models.transfers.results.general.user_system_role import MaleoIdentityUserSystemRoleGeneralResultsTransfers

class MaleoIdentityUserSystemRoleGeneralResultsTypes:
    GetMultiple = Union[
        MaleoIdentityUserSystemRoleGeneralResultsTransfers.Fail,
        MaleoIdentityUserSystemRoleGeneralResultsTransfers.NoData,
        MaleoIdentityUserSystemRoleGeneralResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityUserSystemRoleGeneralResultsTransfers.Fail,
        MaleoIdentityUserSystemRoleGeneralResultsTransfers.NoData,
        MaleoIdentityUserSystemRoleGeneralResultsTransfers.SingleData
    ]

    Assign = Union[
        MaleoIdentityUserSystemRoleGeneralResultsTransfers.Fail,
        MaleoIdentityUserSystemRoleGeneralResultsTransfers.SingleData
    ]