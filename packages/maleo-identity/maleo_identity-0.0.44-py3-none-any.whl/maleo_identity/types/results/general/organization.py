from typing import Union
from maleo_identity.models.transfers.results.general.organization import MaleoIdentityOrganizationGeneralResultsTransfers

class MaleoIdentityOrganizationGeneralResultsTypes:
    GetMultiple = Union[
        MaleoIdentityOrganizationGeneralResultsTransfers.Fail,
        MaleoIdentityOrganizationGeneralResultsTransfers.NoData,
        MaleoIdentityOrganizationGeneralResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityOrganizationGeneralResultsTransfers.Fail,
        MaleoIdentityOrganizationGeneralResultsTransfers.NoData,
        MaleoIdentityOrganizationGeneralResultsTransfers.SingleData
    ]

    GetMultipleStructured = Union[
        MaleoIdentityOrganizationGeneralResultsTransfers.Fail,
        MaleoIdentityOrganizationGeneralResultsTransfers.NoData,
        MaleoIdentityOrganizationGeneralResultsTransfers.MultipleStructured
    ]

    GetSingleStructured = Union[
        MaleoIdentityOrganizationGeneralResultsTransfers.Fail,
        MaleoIdentityOrganizationGeneralResultsTransfers.NoData,
        MaleoIdentityOrganizationGeneralResultsTransfers.SingleStructured
    ]

    CreateOrUpdate = Union[
        MaleoIdentityOrganizationGeneralResultsTransfers.Fail,
        MaleoIdentityOrganizationGeneralResultsTransfers.SingleData
    ]