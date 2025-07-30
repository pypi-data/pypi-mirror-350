from typing import Union
from maleo_identity.models.transfers.results.repository.organization_role import MaleoIdentityOrganizationRoleRepositoryResultsTransfers

class MaleoIdentityOrganizationRoleRepositoryResultsTypes:
    GetMultiple = Union[
        MaleoIdentityOrganizationRoleRepositoryResultsTransfers.Fail,
        MaleoIdentityOrganizationRoleRepositoryResultsTransfers.NoData,
        MaleoIdentityOrganizationRoleRepositoryResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityOrganizationRoleRepositoryResultsTransfers.Fail,
        MaleoIdentityOrganizationRoleRepositoryResultsTransfers.NoData,
        MaleoIdentityOrganizationRoleRepositoryResultsTransfers.SingleData
    ]