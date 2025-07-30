from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.client.service import BaseClientServiceResultsTransfers
from maleo_identity.models.transfers.general.user_organization_role import UserOrganizationRoleTransfers

class MaleoIdentityUserOrganizationRoleClientResultsTransfers:
    class Fail(BaseClientServiceResultsTransfers.Fail): pass

    class NoData(BaseClientServiceResultsTransfers.NoData): pass

    class SingleData(BaseClientServiceResultsTransfers.SingleData):
        data:UserOrganizationRoleTransfers = Field(..., description="Single user organization role data")

    class MultipleData(BaseClientServiceResultsTransfers.PaginatedMultipleData):
        data:list[UserOrganizationRoleTransfers] = Field(..., description="Multiple user organization roles data")