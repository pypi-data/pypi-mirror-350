from typing import Union
from maleo_identity.models.transfers.results.repository.user_organization_role import MaleoIdentityUserOrganizationRoleRepositoryResultsTransfers

class MaleoIdentityUserOrganizationRoleRepositoryResultsTypes:
    GetMultiple = Union[
        MaleoIdentityUserOrganizationRoleRepositoryResultsTransfers.Fail,
        MaleoIdentityUserOrganizationRoleRepositoryResultsTransfers.NoData,
        MaleoIdentityUserOrganizationRoleRepositoryResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityUserOrganizationRoleRepositoryResultsTransfers.Fail,
        MaleoIdentityUserOrganizationRoleRepositoryResultsTransfers.NoData,
        MaleoIdentityUserOrganizationRoleRepositoryResultsTransfers.SingleData
    ]