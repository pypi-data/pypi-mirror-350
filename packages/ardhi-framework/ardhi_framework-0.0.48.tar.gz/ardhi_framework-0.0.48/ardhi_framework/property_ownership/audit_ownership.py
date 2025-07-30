from ardhi_framework.validators import BaseValidatorClass
from ardhi_framework.property_ownership.refactor_ownership import RefactorOwnership


class AuditOwnershipDict(RefactorOwnership, BaseValidatorClass):
    """
    Just raises errors, as defined in exceptions
    """
    def __init__(self, property_ownership: dict or None):
        """This returns all ownership audits of whether valid or not"""

        super(RefactorOwnership, self).__init__(property_ownership)

    def validate_duplicated_owners(self):
        """Check if user is duplicated with the same rights
        Ideally, a user can be duplicated if is an admin for 2 deceased, or if is a
        However, if user is a proprietor, and is duplicated maybe in another share,
        should be flagged.
        Use ownership reviewer to reshape the ownership as desired
        """

    def validate_shares(self):
        """
        FOR TENANTS IN COMMON ONLY
        All shares should pass the following checks:
        1. Shares should total up to 1.00 when evaluated using sympfy if in fraction, 100.00 of in decimal, and no single share should be more than those totals
        2. Shares must be more than one.
        3. Joint common owners own the share jointly. Reviewer should format
        """

    def validate_enumeration_of_all_owners(self):
        """
        All users must be enumerated for any new ownership created. That is, no user without userid in ownership structure
        """


class RebuildOwnershipDict(AuditOwnershipDict):
    """
    This class is used to reshape ownership according to the errors raised in audit,
    and return new structure that is complete and sensible.
    """

    def tenants_to_sole(self):
        """
        This is going to change malformed tenants in common to sole, if user in common is repeated
        """

    def joint_to_sole(self):
        """
        Rare, lRA 38; but confirm ownership is joint if should be sole.
        """

    def add_extra_info(self):
        """
        This is to add some additional information to owner instance (such as admin for deceased...blah blah blah)
        """

