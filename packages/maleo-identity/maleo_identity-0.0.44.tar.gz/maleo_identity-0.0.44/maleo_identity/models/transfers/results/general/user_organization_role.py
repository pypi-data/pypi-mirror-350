from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_identity.models.transfers.general.user_organization_role import UserOrganizationRoleTransfers

class MaleoIdentityUserOrganizationRoleGeneralResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class NoData(BaseServiceGeneralResultsTransfers.NoData): pass

    class SingleData(BaseServiceGeneralResultsTransfers.SingleData):
        data:UserOrganizationRoleTransfers = Field(..., description="Single user organization role data")

    class MultipleData(BaseServiceGeneralResultsTransfers.PaginatedMultipleData):
        data:list[UserOrganizationRoleTransfers] = Field(..., description="Multiple user organization roles data")