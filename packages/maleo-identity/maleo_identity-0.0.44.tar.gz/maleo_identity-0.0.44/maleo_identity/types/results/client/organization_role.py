from typing import Union
from maleo_identity.models.transfers.results.client.organization_role import MaleoIdentityOrganizationRoleClientResultsTransfers

class MaleoIdentityOrganizationRoleClientResultsTypes:
    GetMultiple = Union[
        MaleoIdentityOrganizationRoleClientResultsTransfers.Fail,
        MaleoIdentityOrganizationRoleClientResultsTransfers.NoData,
        MaleoIdentityOrganizationRoleClientResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityOrganizationRoleClientResultsTransfers.Fail,
        MaleoIdentityOrganizationRoleClientResultsTransfers.SingleData
    ]