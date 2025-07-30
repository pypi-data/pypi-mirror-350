"""
Define all exceptions here, for the project, that are common and can be defined
"""
from rest_framework.exceptions import APIException
from ardhi_framework.response import ArdhiResponse as Response
from ardhi_framework.definitions.exceptions import *


class ResponseException(APIException):

    def __init__(self, status=BASE_SYSTEM_ERROR_CODE):
        self.status = status
        self.msg = 'Invalid System data'
        super().__init__()

    def _msg(self):
        return self.msg

    @classmethod
    def error_code_name(cls):
        return cls.__name__.title()

    def status_code(self):
        return self.status

    def __str__(self):
        return self._msg

    def user_msg(self):
        return str(self._msg()) + f'- Error code: {self.status_code()}'

    def response_repr(self):
        return Response({'details': self.user_msg()}, 400)

    def logger_repr(self):
        return f'{self.error_code_name()}: {self.user_msg()}'


class FraudDetectionError(ResponseException):

    def __init__(self, msg):
        self.msg = msg or 'Action terminated prematurely'
        super().__init__(FRAUD_ACTION_CODE)

    def __call__(self, *args, **kwargs):
        # log fraud
        return super().__call__(*args, **kwargs)


class DuplicateOwnerError(ResponseException):

    def __init__(self, msg):
        self.msg = msg or 'One of more users are improperly duplicated'
        super().__init__(O_DUPLICATED_OWNERS_CODE)


class InvalidOwnershipError(ResponseException):

    def __init__(self, msg=None):
        self.msg = msg or 'Ownership structure generated is invalid'
        super().__init__(OWNERSHIP_ERROR_CODE)


class NonEnumeratedOwnerError(ResponseException):
    def __init__(self, msg=None):
        self.msg = msg or 'The system id of one of the users could not be determined.'
        super().__init__(P_ENUMERATION_ERROR_CODE)


class UnauthorizedActorError(ResponseException):
    def __init__(self, msg=None):
        self.msg = msg or 'Unauthorized for this action in this application'
        super().__init__(UNAUTHORIZED_ACTOR_CODE)


class MicroserviceCommunicationError(ResponseException):
    """This is when a system error occurs in inter service call"""
    def __init__(self, msg=None, service_failed=None):
        self.msg = msg or f'Unable to get response from {service_failed}'
        super().__init__(INTER_SERVICES_CONNECTION_ERROR_CODE)


def get_exception_response(exception=None):
    if exception is not None:
        return Response({'details': exception.response_repr()}, 400)
    else:
        return Response({'details': 'Invalid request. Try again later'}, 400)
