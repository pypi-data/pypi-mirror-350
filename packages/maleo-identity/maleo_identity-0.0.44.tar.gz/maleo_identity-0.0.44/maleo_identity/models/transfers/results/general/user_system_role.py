from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_identity.models.transfers.general.user_system_role import UserSystemRoleTransfers

class MaleoIdentityUserSystemRoleGeneralResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class NoData(BaseServiceGeneralResultsTransfers.NoData): pass

    class SingleData(BaseServiceGeneralResultsTransfers.SingleData):
        data:UserSystemRoleTransfers = Field(..., description="Single user system role data")

    class MultipleData(BaseServiceGeneralResultsTransfers.PaginatedMultipleData):
        data:list[UserSystemRoleTransfers] = Field(..., description="Multiple user system roles data")