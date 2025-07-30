from typing import Union
from maleo_identity.models.transfers.results.general.user_organization import MaleoIdentityUserOrganizationGeneralResultsTransfers

class MaleoIdentityUserOrganizationGeneralResultsTypes:
    GetMultiple = Union[
        MaleoIdentityUserOrganizationGeneralResultsTransfers.Fail,
        MaleoIdentityUserOrganizationGeneralResultsTransfers.NoData,
        MaleoIdentityUserOrganizationGeneralResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityUserOrganizationGeneralResultsTransfers.Fail,
        MaleoIdentityUserOrganizationGeneralResultsTransfers.NoData,
        MaleoIdentityUserOrganizationGeneralResultsTransfers.SingleData
    ]

    Assign = Union[
        MaleoIdentityUserOrganizationGeneralResultsTransfers.Fail,
        MaleoIdentityUserOrganizationGeneralResultsTransfers.SingleData
    ]