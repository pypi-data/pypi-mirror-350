from typing import Union
from maleo_identity.models.transfers.results.general.organization_role import MaleoIdentityOrganizationRoleGeneralResultsTransfers

class MaleoIdentityOrganizationRoleGeneralResultsTypes:
    GetMultiple = Union[
        MaleoIdentityOrganizationRoleGeneralResultsTransfers.Fail,
        MaleoIdentityOrganizationRoleGeneralResultsTransfers.NoData,
        MaleoIdentityOrganizationRoleGeneralResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityOrganizationRoleGeneralResultsTransfers.Fail,
        MaleoIdentityOrganizationRoleGeneralResultsTransfers.NoData,
        MaleoIdentityOrganizationRoleGeneralResultsTransfers.SingleData
    ]