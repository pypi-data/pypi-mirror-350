from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.client.service import BaseClientServiceResultsTransfers
from maleo_identity.models.transfers.general.organization_role import OrganizationRoleTransfers

class MaleoIdentityOrganizationRoleClientResultsTransfers:
    class Fail(BaseClientServiceResultsTransfers.Fail): pass

    class NoData(BaseClientServiceResultsTransfers.NoData): pass

    class SingleData(BaseClientServiceResultsTransfers.SingleData):
        data:OrganizationRoleTransfers = Field(..., description="Single organization role data")

    class MultipleData(BaseClientServiceResultsTransfers.PaginatedMultipleData):
        data:list[OrganizationRoleTransfers] = Field(..., description="Multiple organization roles data")