from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_identity.models.transfers.general.organization import OrganizationTransfers, StructuredOrganizationTransfers

class MaleoIdentityOrganizationGeneralResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class NoData(BaseServiceGeneralResultsTransfers.NoData): pass

    class SingleData(BaseServiceGeneralResultsTransfers.SingleData):
        data:OrganizationTransfers = Field(..., description="Single organization data")

    class MultipleData(BaseServiceGeneralResultsTransfers.PaginatedMultipleData):
        data:list[OrganizationTransfers] = Field(..., description="Multiple organizations data")

    class SingleStructured(BaseServiceGeneralResultsTransfers.SingleData):
        data:StructuredOrganizationTransfers = Field(..., description="Single structured organization data")

    class MultipleStructured(BaseServiceGeneralResultsTransfers.PaginatedMultipleData):
        data:list[StructuredOrganizationTransfers] = Field(..., description="Multiple structured organizations data")