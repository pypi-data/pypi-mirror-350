from __future__ import annotations

import uuid
from ..exceptions import InvalidOwnershipError
from ..definitions.ownership import *
from .refactor_ownership import RefactorOwnership


class PropertyOwnershipUtil(RefactorOwnership):

    """
    Provides a validation interface for ownerships
    """
    def __init__(self, property_ownership):
        super().__init__(property_ownership)

    def get_holding_type(self) -> TENANTS_IN_COMMON_TYPE or SOLE_OWNERSHIP_TYPE or JOINT_TENANCY_TYPE or 'UNKNOWN':
        """
        Returns: str - holding type of the ownership instance
        """
        if self.ownership:
            return self.ownership.get('holding_type')
        return 'UNKNOWN'

    def _is_common_holding(self):
        """
        Checks if ownership is tenants in common holding type
        Returns:
            True or false: bool
        """
        return self.get_holding_type() == TENANTS_IN_COMMON_TYPE

    def _is_sole_holding(self):
        """
        Checks if ownership is sole ownership holding type
        Returns:
            True or false: bool
        """
        return self.get_holding_type() == SOLE_OWNERSHIP_TYPE

    def _is_joint_holding(self):
        """
        Checks if ownership is joint tenancy holding type
        Returns:
            True or false: bool
        """
        return self.get_holding_type() == JOINT_TENANCY_TYPE

    def return_owners_instances(self) -> list:
        """
        Returns a primitive list of owners at base - sole or joint or tenants in common
        Returns:
            owners: list
        """
        if self._is_common_holding():
            return list([share['owners'] for share in self.ownership.get('proprietorship_common_owners')])
        elif self._is_sole_holding() or self._is_joint_holding():
            return list(self.ownership.get('proprietors_sole_joint'))
        raise InvalidOwnershipError('Invalid ownership holding type')

    def return_user_owner_instance(self, u_id: str) -> dict or None:
        """
        Returns an owner instance of a user, if exists, else None
        Args:
            u_id:
        Returns: {'user_id': u_id, 'ownership_rights': rights, digitizing_information: {}} or None: dict or None:
        """
        user = list([o for o in self.return_owners_instances() if o['user_id'] == u_id])
        if user:
            return user[0]
        return None

    def is_owner(self, u_id: str | uuid.UUID) -> bool:
        """
        Checks if user is one of the current owners
        Args:
            u_id:
        Returns:
            bool
        """
        return bool(self.return_user_owner_instance(u_id))

    def is_sole_owner(self, u_id: str | uuid.UUID) -> bool:
        """Check if user is the sole owner
        Args:
            u_id - user id of the user being tested
        Returns:
             bool - True if user exists
        """
        return self._is_sole_holding() and self.is_owner(u_id)

    def is_joint_owner(self, u_id: str | uuid.UUID) -> bool:
        """Check if user is one of the joint owners
        @accepts user id u_id
        @returns bool
        """
        return self._is_joint_holding() and self.is_owner(u_id)

    def is_common_owner(self, u_id: str | uuid.UUID) -> bool:
        """Check if user is one of the tenants in common
        @accepts user id u_id
        @returns bool
        """
        return self._is_common_holding() and self.is_owner(u_id)

    def is_admin_owner(self, u_id: str | uuid.UUID) -> bool:
        """
        Confirms user is owner with rights of an administrator
        Args:
            u_id: user id of the user
        Returns:
            True/False:
        """
        return self.is_owner(u_id) and self._owner_rights(u_id) == ADMINISTRATOR_RIGHTS

    def _owner_rights(self, u_id: str | uuid.UUID) -> str or None:
        """
        Returns the ownership rights of a user in an ownership
        Args:
            u_id:
        Returns:
            str: the ownership rights
        """
        if self.is_owner(u_id):
            return self.return_user_owner_instance(u_id).get('ownership_rights')
        return None

    def confirm_ownership_rights(self, u_id: str | uuid.UUID, o_rights: str) -> bool:
        """
        Checks current rights against the required ownership rights
        Args:
            u_id: user id
            o_rights: the ownership rights to be confirmed
        Returns:
            True/False: if matches
        """
        return bool(self._owner_rights(u_id) == o_rights)

