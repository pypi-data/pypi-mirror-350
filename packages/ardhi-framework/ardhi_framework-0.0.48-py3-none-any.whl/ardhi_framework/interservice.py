from datetime import timedelta, datetime

import requests
from django.conf import settings

from ardhi_framework.utils import refine_user, MakeExternalCall

CACHE_EXP = timedelta(minutes=10)
CACHE = {'exp': datetime.now() + CACHE_EXP, 'user_ids': {}}

ACL_BASE_URL = settings.SERVICE_URLS['ACL_BASE_URL']
INVOICE_URL = settings.SERVICE_URLS['PAYMENT_SERVICE_URL']
NOTIFICATIONS_URL = settings.SERVICE_URLS['SHARED_SERVER_URL']
SHARED_SERVER_URL = settings.SERVICE_URLS['SHARED_SERVER_URL']

REGISTRATION_SERVICE = settings.SERVICE_URLS['REGISTRATION_SERVICE']


def check_authenticated(headers):
    url = ACL_BASE_URL + 'auth/' + 'status'
    return MakeExternalCall(method='GET', params={}, headers=headers, url=url).make_api_call()


def get_user_profile(user_id, headers):
    url = ACL_BASE_URL + 'accounts/userminiprofiledetails'
    param = {
        'userid': user_id
    }
    try:
        profile_response = requests.get(url=url, headers=headers, params=param)
    except requests.exceptions.RequestException as e:
        return False
    if profile_response.status_code == 200:
        user_details = profile_response.json()
        user_details['is_refined'] = False
        return refine_user(user_details)
    else:
        return False


def get_document_details(doc_id, headers):
    url = SHARED_SERVER_URL + 'file-upload/document-detail'
    params = {'doc_id': doc_id}
    return MakeExternalCall(method='GET', params=params, headers=headers, url=url).make_api_call()


def get_document_link(doc_id, headers):
    success, doc_details = get_document_details(
        doc_id=doc_id,
        headers=headers
    )
    if not success:
        return None
    else:
        return doc_details['file']


def registration_property_details(headers, property_number):
    url = settings.SERVICE_URLS['REGISTER_SERVICE'] + 'registration-generic/property-details/get_property_details'
    params = {'property_number': property_number}
    return MakeExternalCall(method='GET', params=params, headers=headers, url=url).make_api_call()


def survey_details(headers, parcel_number):
    url = settings.SERVICE_URLS['CADASTRE_SERVICE_URL'] + 'routing/property/status'
    params = { 'property_number': parcel_number }
    return MakeExternalCall(method='GET', params=params, headers=headers, url=url).make_api_call()


def get_parcel_invoices_status(parcel_number, invoice_status=None, page_size=5, headers=None, multiple_status=None):
    url = INVOICE_URL + 'invoicing'
    params = {
        'parcel_number': parcel_number,
        'invoice_status': invoice_status,
        'page_size': page_size,
        'multiple_status': multiple_status
    }
    return MakeExternalCall(method='GET', params=params, headers=headers, url=url).make_api_call()


class Notification:
    def __init__(self, headers, message=None, user_id=None, process=None, task_id=None, notification_type=None,
                 data=None):
        self.headers = headers
        self.message = message
        self.user_id = user_id
        self.process = process
        self.task_id = task_id
        self.notification_type = notification_type
        self.data = data

    def send_notification(self):
        url = settings.SERVICE_URLS['SHARED_SERVER_URL'] + 'notifications_system/add_notification'

        json = {
            'message': self.message,
            'user_id': self.user_id,
            'process': self.process,
            'task_id': self.task_id,
            'notification_type': self.notification_type
        }
        return MakeExternalCall(method='POST', data=json, headers=self.headers, url=url).make_api_call()

    def send_bulk_notification(self):

        url = settings.SERVICE_URLS['SHARED_SERVER_URL'] + 'notifications_system/add_bulk_notification'
        return MakeExternalCall(method='POST', data=self.data, headers=self.headers, url=url).make_api_call()




