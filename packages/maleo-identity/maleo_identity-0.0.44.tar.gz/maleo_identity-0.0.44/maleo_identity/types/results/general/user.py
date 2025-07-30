from typing import Union
from maleo_identity.models.transfers.results.general.user import MaleoIdentityUserGeneralResultsTransfers

class MaleoIdentityUserGeneralResultsTypes:
    GetMultiple = Union[
        MaleoIdentityUserGeneralResultsTransfers.Fail,
        MaleoIdentityUserGeneralResultsTransfers.NoData,
        MaleoIdentityUserGeneralResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityUserGeneralResultsTransfers.Fail,
        MaleoIdentityUserGeneralResultsTransfers.NoData,
        MaleoIdentityUserGeneralResultsTransfers.SingleData
    ]

    CreateOrUpdate = Union[
        MaleoIdentityUserGeneralResultsTransfers.Fail,
        MaleoIdentityUserGeneralResultsTransfers.SingleData
    ]

    GetSinglePassword = Union[
        MaleoIdentityUserGeneralResultsTransfers.Fail,
        MaleoIdentityUserGeneralResultsTransfers.SinglePassword
    ]