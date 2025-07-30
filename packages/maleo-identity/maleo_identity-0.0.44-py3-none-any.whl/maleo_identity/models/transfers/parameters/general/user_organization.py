from __future__ import annotations
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_identity.models.schemas.general import MaleoIdentityGeneralSchemas
from maleo_identity.models.schemas.user_organization import MaleoIdentityUserOrganizationSchemas

class MaleoIdentityUserOrganizationGeneralParametersTransfers:
    class GetSingleQuery(
        MaleoIdentityUserOrganizationSchemas.Expand,
        BaseParameterSchemas.OptionalListOfStatuses
    ): pass

    class GetSingle(
        MaleoIdentityUserOrganizationSchemas.Expand,
        BaseParameterSchemas.OptionalListOfStatuses,
        MaleoIdentityGeneralSchemas.OrganizationId,
        MaleoIdentityGeneralSchemas.UserId
    ): pass

    class AssignQuery(
        MaleoIdentityUserOrganizationSchemas.Expand
    ): pass

    class AssignData(
        MaleoIdentityGeneralSchemas.OrganizationId,
        MaleoIdentityGeneralSchemas.UserId
    ): pass

    class Assign(
        AssignData,
        AssignQuery
    ): pass