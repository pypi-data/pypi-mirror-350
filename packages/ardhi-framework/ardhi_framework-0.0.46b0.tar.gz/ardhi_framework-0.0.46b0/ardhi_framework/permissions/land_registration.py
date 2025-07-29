
"""
Land registration department permissions
"""
from ardhi_framework.permissions.base_permissions import PublicProfessionalPermission, StaffPermission, \
    ReadOnlyPermission, DepartmentHeadPermission


class AdvocatePermission(PublicProfessionalPermission):
    role_name = 'PUBLIC_ADVOCATE'


class InvestigationOfficerPermission(StaffPermission):
    role_name = 'INVESTIGATION_OFFICER'


class RegistrarPermission(StaffPermission):
    role_name = 'REGISTRAR'


class CLRPermission(StaffPermission, ReadOnlyPermission, DepartmentHeadPermission):
    role_name = 'CLR'


class HeadOfStampDutyPermission(StaffPermission):
    role_name = 'HEAD_OF_STAMP_DUTY'


