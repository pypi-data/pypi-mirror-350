from typing import Union
from maleo_identity.models.transfers.results.repository.user_organization import MaleoIdentityUserOrganizationRepositoryResultsTransfers

class MaleoIdentityUserOrganizationRepositoryResultsTypes:
    GetMultiple = Union[
        MaleoIdentityUserOrganizationRepositoryResultsTransfers.Fail,
        MaleoIdentityUserOrganizationRepositoryResultsTransfers.NoData,
        MaleoIdentityUserOrganizationRepositoryResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityUserOrganizationRepositoryResultsTransfers.Fail,
        MaleoIdentityUserOrganizationRepositoryResultsTransfers.NoData,
        MaleoIdentityUserOrganizationRepositoryResultsTransfers.SingleData
    ]

    Assign = Union[
        MaleoIdentityUserOrganizationRepositoryResultsTransfers.Fail,
        MaleoIdentityUserOrganizationRepositoryResultsTransfers.SingleData
    ]