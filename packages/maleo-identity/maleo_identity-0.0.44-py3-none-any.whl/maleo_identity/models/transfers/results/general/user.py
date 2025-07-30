from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_identity.models.transfers.general.user import UserTransfers, PasswordTransfers

class MaleoIdentityUserGeneralResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class NoData(BaseServiceGeneralResultsTransfers.NoData): pass

    class SingleData(BaseServiceGeneralResultsTransfers.SingleData):
        data:UserTransfers = Field(..., description="Single user data")

    class MultipleData(BaseServiceGeneralResultsTransfers.PaginatedMultipleData):
        data:list[UserTransfers] = Field(..., description="Multiple users data")

    class SinglePassword(BaseServiceGeneralResultsTransfers.SingleData):
        data:PasswordTransfers = Field(..., description="Single user password")