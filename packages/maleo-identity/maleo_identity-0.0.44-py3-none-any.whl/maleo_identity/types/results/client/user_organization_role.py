from typing import Union
from maleo_identity.models.transfers.results.client.user_organization_role import MaleoIdentityUserOrganizationRoleClientResultsTransfers

class MaleoIdentityUserOrganizationRoleClientResultsTypes:
    GetMultiple = Union[
        MaleoIdentityUserOrganizationRoleClientResultsTransfers.Fail,
        MaleoIdentityUserOrganizationRoleClientResultsTransfers.NoData,
        MaleoIdentityUserOrganizationRoleClientResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityUserOrganizationRoleClientResultsTransfers.Fail,
        MaleoIdentityUserOrganizationRoleClientResultsTransfers.SingleData
    ]