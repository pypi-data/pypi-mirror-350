
"""

Surveying department permissions
"""
from ardhi_framework.permissions.base_permissions import PublicProfessionalPermission, StaffPermission, \
    DepartmentHeadPermission


class LicensedSurveyorPermission(PublicProfessionalPermission):
    role_name = 'PUBLIC_LICENSED_SURVEYOR'


class GovernmentSurveyorPermission(StaffPermission):
    role_name = 'GOVERNMENT_SURVEYOR'


class DOSPermission(StaffPermission, DepartmentHeadPermission):
    role_name = 'DOS'


class CartographySROPermission(StaffPermission):
    role_name = 'CARTOGRAPHY_SRO'


class CheckerPermission(StaffPermission):
    role_name = 'CHECKER'

