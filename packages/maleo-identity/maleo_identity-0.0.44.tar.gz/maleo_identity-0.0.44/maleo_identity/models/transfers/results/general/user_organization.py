from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_identity.models.transfers.general.user_organization import UserOrganizationTransfers

class MaleoIdentityUserOrganizationGeneralResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class NoData(BaseServiceGeneralResultsTransfers.NoData): pass

    class SingleData(BaseServiceGeneralResultsTransfers.SingleData):
        data:UserOrganizationTransfers = Field(..., description="Single user organization data")

    class MultipleData(BaseServiceGeneralResultsTransfers.PaginatedMultipleData):
        data:list[UserOrganizationTransfers] = Field(..., description="Multiple user organizations data")