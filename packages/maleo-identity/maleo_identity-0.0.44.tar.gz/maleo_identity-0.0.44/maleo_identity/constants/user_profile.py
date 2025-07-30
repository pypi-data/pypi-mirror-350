from typing import Dict
from maleo_identity.enums.user_profile import MaleoIdentityUserProfileEnums

class MaleoIdentityUserProfileConstants:
    IDENTIFIER_TYPE_VALUE_TYPE_MAP:Dict[
        MaleoIdentityUserProfileEnums.IdentifierType,
        object
    ] = {
        MaleoIdentityUserProfileEnums.IdentifierType.USER_ID: int,
        MaleoIdentityUserProfileEnums.IdentifierType.ID_CARD: str,
    }