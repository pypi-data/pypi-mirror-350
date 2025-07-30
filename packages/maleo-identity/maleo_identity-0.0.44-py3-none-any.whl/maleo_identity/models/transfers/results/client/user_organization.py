from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.client.service import BaseClientServiceResultsTransfers
from maleo_identity.models.transfers.general.user_organization import UserOrganizationTransfers

class MaleoIdentityUserOrganizationClientResultsTransfers:
    class Fail(BaseClientServiceResultsTransfers.Fail): pass

    class NoData(BaseClientServiceResultsTransfers.NoData): pass

    class SingleData(BaseClientServiceResultsTransfers.SingleData):
        data:UserOrganizationTransfers = Field(..., description="Single user organization data")

    class MultipleData(BaseClientServiceResultsTransfers.PaginatedMultipleData):
        data:list[UserOrganizationTransfers] = Field(..., description="Multiple user organizations data")