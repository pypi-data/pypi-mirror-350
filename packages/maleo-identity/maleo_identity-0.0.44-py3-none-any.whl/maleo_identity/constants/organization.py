from typing import Dict
from uuid import UUID
from maleo_identity.enums.organization import MaleoIdentityOrganizationEnums

class MaleoIdentityOrganizationConstants:
    IDENTIFIER_TYPE_VALUE_TYPE_MAP:Dict[
        MaleoIdentityOrganizationEnums.IdentifierType,
        object
    ] = {
        MaleoIdentityOrganizationEnums.IdentifierType.ID: int,
        MaleoIdentityOrganizationEnums.IdentifierType.UUID: UUID,
        MaleoIdentityOrganizationEnums.IdentifierType.KEY: str
    }