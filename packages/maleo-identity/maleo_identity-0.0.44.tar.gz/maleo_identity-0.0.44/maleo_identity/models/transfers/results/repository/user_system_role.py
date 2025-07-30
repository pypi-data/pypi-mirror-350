from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.service.repository import BaseServiceRepositoryResultsTransfers
from maleo_identity.models.transfers.general.user_system_role import UserSystemRoleTransfers

class MaleoIdentityUserSystemRoleRepositoryResultsTransfers:
    class Fail(BaseServiceRepositoryResultsTransfers.Fail): pass

    class NoData(BaseServiceRepositoryResultsTransfers.NoData): pass

    class SingleData(BaseServiceRepositoryResultsTransfers.SingleData):
        data:UserSystemRoleTransfers = Field(..., description="Single user system role data")

    class MultipleData(BaseServiceRepositoryResultsTransfers.PaginatedMultipleData):
        data:list[UserSystemRoleTransfers] = Field(..., description="Multiple user system roles data")