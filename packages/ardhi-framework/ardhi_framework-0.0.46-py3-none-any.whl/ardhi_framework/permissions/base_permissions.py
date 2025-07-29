from rest_framework import permissions

from ardhi_framework.interservice import check_authenticated
from ardhi_framework.utils import decode_jwt, check_common_member_sets


class AuthenticatedUserPermission(permissions.BasePermission):
    message = 'Unauthorised User Not Allowed.'

    def has_permission(self, request, view):
        if 'Authorization' not in request.headers.keys() and 'JWTAUTH' not in request.headers.keys():
            return False
        headers = {
            'Authorization': request.headers.get('Authorization'),
            'JWTAUTH': request.headers.get('JWTAUTH')
        }
        try:
            return check_authenticated(headers)
        except:
            return False


class StaffPermission(AuthenticatedUserPermission):
    """
    Represents a staff member's permission system.

    The StaffPermission class manages the permissions associated with staff
    members. It provides a framework for defining and managing the access
    rights and restrictions that are applicable to staff users in a given
    context. This class is typically used in systems where role-based
    access control is enforced.
    """
    user_type = 'STAFF'
    role_names = []

    def has_permission(self, request, view):
        if super().has_permission(request, view):
            user_details = decode_jwt(request.headers.get('JWTAUTH').split(' ')[1])
            roles_list = [x['groupname'] for x in user_details['roles']]
            if self.user_type == 'COUNTY_STAFF':
                if not user_details.get('ardhipay_roles'):  # not staff
                    return False
                roles_list.extend([x['groupname'] for x in user_details['ardhipay_roles']])

            elif not user_details.get('organization'):  # not staff
                return False

            return check_common_member_sets(self.role_names, roles_list) if bool(self.role_names) else True
        return False


class PublicUserPermission(AuthenticatedUserPermission):
    """
    Represents public user permissions.

    This class is designed to handle the permissions associated with a public user
    within a system. It defines the permission levels that a user can have,
    allowing them access to different parts of the application based on their
    role and assigned rights.

    """
    user_type = 'PUBLIC'


class PublicProfessionalPermission(AuthenticatedUserPermission):
    # EG A public advocate, public licensed surveyor
    """
    Represents permissions and roles assigned to a public professional.

    This class defines the roles and responsibilities specific to
    public professionals such as public advocates or public licensed
    surveyors. It encapsulates permissions and functionalities
    relevant to these roles, enabling precise access control and
    regulation adherence.
    """
    user_type = 'PROFESSIONAL'
    role_names = []


class DepartmentHeadPermission(StaffPermission):
    # for depeartment heads with superintendent powers
    """
    Represents permission levels for department heads, including
    superintendent powers.

    This class is designed to handle and define the set of permissions for
    department heads who are endowed with superintendent-level authority.
    It sets a structure for managing and distinguishing these permissions
    in a system where roles and responsibilities are distributed.

    Attributes:
        None
    """
    role_names = []


class ReadOnlyPermission(AuthenticatedUserPermission):
    # to control view and action for read only
    """
    Controls view and action permissions to enable read-only access.

    This class is designed to handle and enforce read-only permissions for
    specific use cases. It ensures that users can only perform actions that
    do not alter the state or modify resources. Typically used in scenarios
    where viewing data is permitted, but editing is restricted. The purpose
    is to maintain data integrity while allowing necessary visibility.

    Attributes
    ----------
    None
    """



