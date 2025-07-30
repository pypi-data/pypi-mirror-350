from ardhi_framework.property_ownership.refactor_ownership import RefactorOwnership

"""
    THE USE OF THIS CODE:
    This code is used for displays in registers, titles and other documents that require formatted text such as :
    OWNER1 and OWNER 2 as administrators for the estate of the late OWNER0;
    or 
    OWNER-A, OWNER-B and OWNER-C (Tenants in common, Jointly) - 1/2 share;

"""
class FormatOwnership(RefactorOwnership):

    def format_sole_owner(self, inst: dict):
        """
        Takes in an ownership instance, and returns a phrase of the owner's names and ownership type - sole
        However, if admin, confirms multiple owners, and adds additional information if available for the deceased
        Args:
            inst: dict - ownership instance
        Returns:
            human-readable shape
        """

    def format_joint_owners(self, inst: list):
        """
        Takes a list of the dictionaries, of the owners to be labelled as joint owners;
        Args:
            inst: list
        Returns: str
        """

    def format_admins_of_joint_owners(self, inst: list):
        """
        Suppose after LRA 39, joint owners are deceased, the admins belong to each deceased, even if repeated
        Args:
            inst: list
        Returns:
        """

    def format_tenants_in_common_sole(self, inst: dict):
        """
        Return formatted sole owners of tenant share
        """

    def format_tenants_in_common_joint(self, inst: dict):
        """
        If two proprietors hold same share, then format as per share and joint
        """

