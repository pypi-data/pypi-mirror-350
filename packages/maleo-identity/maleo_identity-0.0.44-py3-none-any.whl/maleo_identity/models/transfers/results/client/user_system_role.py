from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.client.service import BaseClientServiceResultsTransfers
from maleo_identity.models.transfers.general.user_system_role import UserSystemRoleTransfers

class MaleoIdentityUserSystemRoleClientResultsTransfers:
    class Fail(BaseClientServiceResultsTransfers.Fail): pass

    class NoData(BaseClientServiceResultsTransfers.NoData): pass

    class SingleData(BaseClientServiceResultsTransfers.SingleData):
        data:UserSystemRoleTransfers = Field(..., description="Single user system role data")

    class MultipleData(BaseClientServiceResultsTransfers.PaginatedMultipleData):
        data:list[UserSystemRoleTransfers] = Field(..., description="Multiple user system roles data")