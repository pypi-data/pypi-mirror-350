from typing import Union
from maleo_identity.models.transfers.results.client.user_organization import MaleoIdentityUserOrganizationClientResultsTransfers

class MaleoIdentityUserOrganizationClientResultsTypes:
    GetMultiple = Union[
        MaleoIdentityUserOrganizationClientResultsTransfers.Fail,
        MaleoIdentityUserOrganizationClientResultsTransfers.NoData,
        MaleoIdentityUserOrganizationClientResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityUserOrganizationClientResultsTransfers.Fail,
        MaleoIdentityUserOrganizationClientResultsTransfers.SingleData
    ]

    Assign = Union[
        MaleoIdentityUserOrganizationClientResultsTransfers.Fail,
        MaleoIdentityUserOrganizationClientResultsTransfers.SingleData
    ]