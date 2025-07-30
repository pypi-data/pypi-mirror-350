from abc import ABC
from ardhi_framework.request import ArdhiRequest


class RequestUpdate(ABC):
    """
    Class to update application details and related functions
    """
    request: ArdhiRequest = None
    application_request = None

    def __init__(self, context: dict):
        self.context = context

    def add_remark(self, rmk: str, status: str) -> tuple[bool, str]:
        """Adds actor remark using logged in role param"""
        self.request.remarks.create(
            status=status,
            actor_id=self.context['user'],
            actor_role=self.context['active_role'],
            remarks=rmk
        )
        return True, 'Saved successfully'

    def authenticate(self):
        pass


