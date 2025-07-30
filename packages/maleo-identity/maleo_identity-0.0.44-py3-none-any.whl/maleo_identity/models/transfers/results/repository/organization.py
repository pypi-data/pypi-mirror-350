from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.service.repository import BaseServiceRepositoryResultsTransfers
from maleo_identity.models.transfers.general.organization import OrganizationTransfers, StructuredOrganizationTransfers

class MaleoIdentityOrganizationRepositoryResultsTransfers:
    class Fail(BaseServiceRepositoryResultsTransfers.Fail): pass

    class NoData(BaseServiceRepositoryResultsTransfers.NoData): pass

    class SingleData(BaseServiceRepositoryResultsTransfers.SingleData):
        data:OrganizationTransfers = Field(..., description="Single organization data")

    class MultipleData(BaseServiceRepositoryResultsTransfers.PaginatedMultipleData):
        data:list[OrganizationTransfers] = Field(..., description="Multiple organizations data")

    class SingleStructured(BaseServiceRepositoryResultsTransfers.SingleData):
        data:StructuredOrganizationTransfers = Field(..., description="Single structured organization data")

    class MultipleStructured(BaseServiceRepositoryResultsTransfers.PaginatedMultipleData):
        data:list[StructuredOrganizationTransfers] = Field(..., description="Multiple structured organizations data")