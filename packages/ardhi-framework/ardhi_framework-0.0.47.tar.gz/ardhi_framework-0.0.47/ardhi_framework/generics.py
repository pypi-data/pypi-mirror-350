import base64
import json
import logging

from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView

from ardhi_framework.response import ArdhiResponse
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from django.views.generic import View
from ardhi_framework.models import ArdhiBaseModel
from ardhi_framework.utils import format_error, decode_jwt


class ArdhiGeneralView(View):
    pass


class ArdhiBaseView(ArdhiGeneralView):
    # requires that each function to have serializer_class and return success message
    serializer_class = None

    def get_serializer_context(self):
        context = {
            'headers': self.return_headers,
            'user': self.logged_in_user,
            'request_id': self.request_id,
            'request': None,
            'method': self.request.method,
            'active_role': self.active_role,
            'is_staff': self.is_staff,
        }
        return context

    @property
    def is_staff(self):
        return bool(
            decode_jwt(self.return_headers.get('JWTAUTH').split(' ')[1]).get('organization', False))  # not staff

    @property
    def active_role(self):
        if self.return_headers.get('CPARAMS', None) is not None:
            return json.loads((base64.b64decode(self.return_headers.get('CPARAMS').encode()).decode('utf-8')))['active_role']
        return 'UNKNOWN_ROLE'

    @property
    def request_id(self, req_id=None):
        if not req_id:
            return self.request.query_params.get('request_id', self.request.data.get('request_id', None))
        return req_id

    @property
    def logged_in_user(self):
        return decode_jwt(self.return_headers.get('JWTAUTH').split(' ')[1]).get('user')

    @property
    def context(self):
        return self.get_serializer_context()

    @property
    def return_headers(self):
        headers = {
            'Authorization': self.request.headers.get('Authorization'),
            'JWTAUTH': self.request.headers.get('JWTAUTH'),
            'CPARAMS': self.request.headers.get('CPARAMS')
        }
        return headers

    @staticmethod
    def return_invalid_serializer(serializer):
        return ArdhiResponse({'details': format_error(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def return_failed(created_response):
        return ArdhiResponse({'details': created_response}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def return_success(data):
        return ArdhiResponse(data, status=status.HTTP_200_OK)

    def run_serializer_validator(self, success_msg=None):
        """Processes the serializer through validation to save"""
        context = self.get_serializer_context()
        with transaction.atomic():
            sp = transaction.savepoint()
            try:
                if context['method'] == 'PATCH':
                    self.serializer_class = self.delete_serializer or None
                serializer = self.get_serializer_class()(
                    data=self.request.data,
                    context=context
                )
                # prevent assertion error for the next code
                if not bool(self.request.data):
                    transaction.savepoint_rollback(sp)
                    return self.return_failed('Data is required')

                if not serializer.is_valid():
                    transaction.savepoint_rollback(sp)
                    return self.return_invalid_serializer(serializer)

                created, created_response = serializer.save()
                if not created:
                    transaction.savepoint_rollback(sp)
                    return self.return_failed(created_response)
                if created_response is not None:
                    if isinstance(created_response, dict):
                        created_response['details'] = success_msg
                        return self.return_success(created_response)
                    elif isinstance(created_response, str):
                        return self.return_success({"details": created_response})
            except Exception as e:
                transaction.savepoint_rollback(sp)
                logging.error(e)
                return self.return_failed('Unknown error occurred. Try again later')
            return self.return_success({"details": success_msg})


class ArdhiGenericViewSet(ArdhiBaseView, GenericViewSet):
    """Generic viewset uses action decorators. Modified here"""
    pass


class ArdhiAPIView(ArdhiBaseView, APIView):

    def delete(self, request, *args, **kwargs):
        """No delete method allowed. Override destroy method to perform delete action."""
        return self.return_success('Deleted successfully.')  # we now it has skipped deletion


class ArdhiModelViewSet(ArdhiBaseView, ModelViewSet):
    model: ArdhiBaseModel = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def perform_destroy(self, request, *args, **kwargs):
        # ensure no delete occurs by overriding destroy method
        return


