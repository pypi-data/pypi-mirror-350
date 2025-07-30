from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.client.service import BaseClientServiceResultsTransfers
from maleo_identity.models.transfers.general.user_profile import UserProfileTransfers

class MaleoIdentityUserProfileClientResultsTransfers:
    class Fail(BaseClientServiceResultsTransfers.Fail): pass

    class NoData(BaseClientServiceResultsTransfers.NoData): pass

    class SingleData(BaseClientServiceResultsTransfers.SingleData):
        data:UserProfileTransfers = Field(..., description="Single user profile data")

    class MultipleData(BaseClientServiceResultsTransfers.PaginatedMultipleData):
        data:list[UserProfileTransfers] = Field(..., description="Multiple user profiles data")