from typing import Dict, List
from maleo_identity.enums.user import MaleoIdentityUserEnums
from maleo_identity.enums.organization import MaleoIdentityOrganizationEnums
from maleo_identity.enums.user_organization import MaleoIdentityUserOrganizationEnums

class MaleoIdentityUserOrganizationConstants:
    EXPANDABLE_FIELDS_DEPENDENCIES_MAP:Dict[
        MaleoIdentityUserOrganizationEnums.ExpandableFields,
        List[MaleoIdentityUserOrganizationEnums.ExpandableFields]
    ] = {
        MaleoIdentityUserOrganizationEnums.ExpandableFields.USER: [
            MaleoIdentityUserOrganizationEnums.ExpandableFields.USER_TYPE
        ],
        MaleoIdentityUserOrganizationEnums.ExpandableFields.ORGANIZATION: [
            MaleoIdentityUserOrganizationEnums.ExpandableFields.ORGANIZATION_TYPE
        ]
    }

    USER_EXPANDABLE_FIELDS_MAP:Dict[
        MaleoIdentityUserOrganizationEnums.ExpandableFields,
        MaleoIdentityUserEnums.ExpandableFields
    ] = {
        MaleoIdentityUserOrganizationEnums.ExpandableFields.USER_TYPE: MaleoIdentityUserEnums.ExpandableFields.USER_TYPE
    }

    ORGANIZATION_EXPANDABLE_FIELDS_MAP:Dict[
        MaleoIdentityUserOrganizationEnums.ExpandableFields,
        MaleoIdentityOrganizationEnums.ExpandableFields
    ] = {
        MaleoIdentityUserOrganizationEnums.ExpandableFields.ORGANIZATION_TYPE: MaleoIdentityOrganizationEnums.ExpandableFields.ORGANIZATION_TYPE
    }