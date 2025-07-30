from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.service.repository import BaseServiceRepositoryResultsTransfers
from maleo_identity.models.transfers.general.user_organization import UserOrganizationTransfers

class MaleoIdentityUserOrganizationRepositoryResultsTransfers:
    class Fail(BaseServiceRepositoryResultsTransfers.Fail): pass

    class NoData(BaseServiceRepositoryResultsTransfers.NoData): pass

    class SingleData(BaseServiceRepositoryResultsTransfers.SingleData):
        data:UserOrganizationTransfers = Field(..., description="Single user organization data")

    class MultipleData(BaseServiceRepositoryResultsTransfers.PaginatedMultipleData):
        data:list[UserOrganizationTransfers] = Field(..., description="Multiple user organizations data")