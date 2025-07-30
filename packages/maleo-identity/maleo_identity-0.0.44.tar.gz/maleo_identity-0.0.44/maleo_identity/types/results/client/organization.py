from typing import Union
from maleo_identity.models.transfers.results.client.organization import MaleoIdentityOrganizationClientResultsTransfers

class MaleoIdentityOrganizationClientResultsTypes:
    GetMultiple = Union[
        MaleoIdentityOrganizationClientResultsTransfers.Fail,
        MaleoIdentityOrganizationClientResultsTransfers.NoData,
        MaleoIdentityOrganizationClientResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityOrganizationClientResultsTransfers.Fail,
        MaleoIdentityOrganizationClientResultsTransfers.SingleData
    ]

    GetMultipleStructured = Union[
        MaleoIdentityOrganizationClientResultsTransfers.Fail,
        MaleoIdentityOrganizationClientResultsTransfers.NoData,
        MaleoIdentityOrganizationClientResultsTransfers.MultipleStructured
    ]

    GetSingleStructured = Union[
        MaleoIdentityOrganizationClientResultsTransfers.Fail,
        MaleoIdentityOrganizationClientResultsTransfers.SingleStructured
    ]

    CreateOrUpdate = Union[
        MaleoIdentityOrganizationClientResultsTransfers.Fail,
        MaleoIdentityOrganizationClientResultsTransfers.SingleData
    ]