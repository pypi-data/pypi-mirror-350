from enum import StrEnum

class MaleoIdentityUserSystemRoleEnums:
    class ExpandableFields(StrEnum):
        USER = "user"
        USER_TYPE = "user.user_type"
        PROFILE = "user.profile"
        GENDER = "user.profile.gender"
        BLOOD_TYPE = "user.profile.blood_type"
        SYSTEM_ROLE = "system_role"