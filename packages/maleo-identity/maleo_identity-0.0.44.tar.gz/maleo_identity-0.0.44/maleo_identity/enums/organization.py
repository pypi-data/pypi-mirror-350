from enum import StrEnum

class MaleoIdentityOrganizationEnums:
    class IdentifierType(StrEnum):
        ID = "id"
        UUID = "uuid"
        KEY = "key"

    class ExpandableFields(StrEnum):
        ORGANIZATION_TYPE = "organization_type"