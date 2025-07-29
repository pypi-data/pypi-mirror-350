from ardhi_framework.generics import ArdhiBaseView
from ardhi_framework.permissions.base_permissions import *


class SystemUserView(ArdhiBaseView):
    """
    Literally, every view and endpoint in the system should inherit from this class.
    This view is also expected to override AllowAny permission class by rest_framework.permissions.AllowAny
    No Allow Any endpoints allowed in the system.
    """
    permission_classes = [AuthenticatedUserPermission, ]


class PublicActorView(SystemUserView):
    """
    The basest class of permissions for a user - public user - Manages permissions and logging if available
    """
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.permission_classes += [PublicUserPermission, ]


class StaffActorView(SystemUserView):
    """
    Base class for staff user views, to manage permissions and logging if available
    """

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.permission_classes += [StaffPermission, ]



