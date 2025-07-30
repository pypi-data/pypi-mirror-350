from typing import Union
from maleo_identity.models.transfers.results.general.user_organization_role import MaleoIdentityUserOrganizationRoleGeneralResultsTransfers

class MaleoIdentityUserOrganizationRoleGeneralResultsTypes:
    GetMultiple = Union[
        MaleoIdentityUserOrganizationRoleGeneralResultsTransfers.Fail,
        MaleoIdentityUserOrganizationRoleGeneralResultsTransfers.NoData,
        MaleoIdentityUserOrganizationRoleGeneralResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityUserOrganizationRoleGeneralResultsTransfers.Fail,
        MaleoIdentityUserOrganizationRoleGeneralResultsTransfers.NoData,
        MaleoIdentityUserOrganizationRoleGeneralResultsTransfers.SingleData
    ]