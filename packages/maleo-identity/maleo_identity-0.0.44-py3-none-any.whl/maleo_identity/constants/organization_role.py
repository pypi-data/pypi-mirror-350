from typing import Dict, List
from maleo_identity.enums.organization import MaleoIdentityOrganizationEnums
from maleo_identity.enums.organization_role import MaleoIdentityOrganizationRoleEnums

class MaleoIdentityOrganizationRoleConstants:
    EXPANDABLE_FIELDS_DEPENDENCIES_MAP:Dict[
        MaleoIdentityOrganizationRoleEnums.ExpandableFields,
        List[MaleoIdentityOrganizationRoleEnums.ExpandableFields]
    ] = {
        MaleoIdentityOrganizationRoleEnums.ExpandableFields.ORGANIZATION: [
            MaleoIdentityOrganizationRoleEnums.ExpandableFields.ORGANIZATION_TYPE
        ]
    }

    ORGANIZATION_EXPANDABLE_FIELDS_MAP:Dict[
        MaleoIdentityOrganizationRoleEnums.ExpandableFields,
        MaleoIdentityOrganizationEnums.ExpandableFields
    ] = {
        MaleoIdentityOrganizationRoleEnums.ExpandableFields.ORGANIZATION_TYPE: MaleoIdentityOrganizationEnums.ExpandableFields.ORGANIZATION_TYPE
    }