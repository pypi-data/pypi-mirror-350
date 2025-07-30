from enum import StrEnum

class MaleoIdentityUserEnums:
    class IdentifierType(StrEnum):
        ID = "id"
        UUID = "uuid"
        USERNAME = "username"
        EMAIL = "email"
        PHONE = "phone"

    class ExpandableFields(StrEnum):
        USER_TYPE = "user_type"
        PROFILE = "profile"
        GENDER = "profile.gender"
        BLOOD_TYPE = "profile.blood_type"