from rest_framework.decorators import action

from ardhi_framework.permissions.base_permissions import AuthenticatedUserPermission, StaffPermission, \
    PublicUserPermission, PublicProfessionalPermission


def custom_view_action(
    methods=('get', 'post', 'put'),
    detail=False,
    url_path=None,
    url_name=None,
    permission_classes=(AuthenticatedUserPermission,),
    **kwargs
):
    """
    A decorator similar to @action, preconfigured for officer actions.
    Sets `func.officer_action = True` and applies DRF's @action decorator,
    while allowing override of permission_classes and other action arguments.
    """

    def decorator(func):
        # Apply DRF's action decorator with the injected/overridable parameters
        decorated = action(
            methods=list(methods),
            detail=detail,
            url_path=url_path,
            url_name=url_name,
            permission_classes=permission_classes,
            **kwargs
        )(func)
        return decorated

    return decorator


def return_decorator(
        methods=('get', 'post', 'put'),
        detail=False,
        url_path=None,
        url_name=None,
        permission_classes=(AuthenticatedUserPermission,),
        **kwargs):

    return custom_view_action(
        methods=list(methods),
        detail=detail,
        url_path=url_path,
        url_name=url_name,
        permission_classes=permission_classes,
        **kwargs)


def officer_action_view(
        actor_roles=None,
        methods=('get', 'post', 'put'),
        detail=False,
        url_path=None,
        url_name=None,
        **kwargs):
    """
    Decorator for officer actions like approve, reject, etc
    """
    StaffPermission.role_names = actor_roles
    permission_classes = [StaffPermission, ]

    return return_decorator(
        methods=list(methods),
        detail=detail,
        url_path=url_path,
        url_name=url_name,
        permission_classes=permission_classes,
        **kwargs)


def public_action_view(
        methods=('get', 'post', 'put'),
        detail=False,
        url_path=None,
        url_name=None,
        **kwargs):
    """
    Action view for public users
    """
    permission_classes = [PublicUserPermission, ]
    return return_decorator(
        methods=list(methods),
        detail=detail,
        url_path=url_path,
        url_name=url_name,
        permission_classes=permission_classes,
        **kwargs)


def professional_action_view(
        actor_roles=None,
        methods=('get', 'post', 'put'),
        detail=False,
        url_path=None,
        url_name=None,
        **kwargs):
    """Action decorator for professional users"""
    PublicProfessionalPermission.role_names = actor_roles
    permission_classes = [PublicProfessionalPermission, ]

    return return_decorator(
        methods=list(methods),
        detail=detail,
        url_path=url_path,
        url_name=url_name,
        permission_classes=permission_classes,
        **kwargs)


def snitch_action(func):
    """
    Decorator to report all actions taken on a parcel, or report
    requires func.parcel_number from the func/class
    """
    parcel_number = func.parcel_number


def states(func):
    """
    Validates and updates states of an application
    Accepts:
    current_node - for validation of permission for action
    next_node - try to automate this. If given, update. If not, maintain the state, pass action
    """


