import random
import string
import jwt
from django.conf import settings
from django.db.models import Model, ForeignKey
from django.forms import model_to_dict
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ErrorDetail
from rest_framework.utils.serializer_helpers import ReturnDict
from copy import deepcopy
import logging
from threading import Timer

import requests


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 20


def random_string_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_reference_number_generator(model, process_prefix, department='LAS'):
    reference_number = department + '/' + process_prefix + '/' + random_string_generator()

    Klass = model

    qs_exists = Klass.objects.filter(reference_number=reference_number).exists()
    if qs_exists:
        return unique_reference_number_generator(model, process_prefix=process_prefix)
    return reference_number


def decode_jwt(jwt_code):
    response = jwt.decode(jwt_code, settings.SECRET_KEY, algorithms='HS256', options={"verify_signature": False, "verify_exp": False})
    return response


def format_error(errors):
    if type(errors) == str:
        return errors
    elif (type(errors) == ReturnDict) or (type(errors) == dict):
        return get_error_message_from_dict(dict(errors))
    return get_error_message_from_dict(errors)


def get_error_message_from_dict(error):
    if type(error) == str:
        return error
    finished_processed_errors = []
    list_of_string_objects = [error]
    count = 0
    processing = True
    while processing:
        # print('list_of_string_objects:-> ', list_of_string_objects)
        for index, i in enumerate(list_of_string_objects):
            if type(i) == str:
                finished_processed_errors.append(list_of_string_objects.pop(index))
                continue
            if type(i) == dict:
                # print("object being processed:->", i)
                list_of_string_objects.append(recursive_dict_error(i))
                list_of_string_objects.pop(index)
            elif type(i) == list:
                list_of_string_objects.append(recursive_list_error(i))
                list_of_string_objects.pop(index)
            else:
                list_of_string_objects.append(str(i))
                list_of_string_objects.pop(index)
            del i
        count += 1
        if count > 20:
            processing = False
    # print('finished_processed_errors:-> ', finished_processed_errors)
    # print('finished_processed_errors:-> ', finished_processed_errors)
    final_error = ''.join(finished_processed_errors)
    return final_error


def recursive_dict_error(error):
    copy_of_error = deepcopy(error)
    if isinstance(error, dict):
        stored_keys = tuple(copy_of_error.keys())
        string_list_objects = []
        value_ = None
        for i in stored_keys:
            # print('type:-> ', type(copy_of_error[i]))
            if type(copy_of_error[i]) == list:
                # print('type:-> ', tuple(copy_of_error[i]))
                copy_of_error[i] = list(filter(None, copy_of_error[i]))
                for indiv in copy_of_error[i]:
                    if type(indiv) == ErrorDetail:
                        if i == 'non_field_errors':
                            value_ = str(indiv)
                        else:
                            value_ = str(i).capitalize().replace("_", " ") + " : " + str(indiv)
                    else:
                        if i == 'non_field_errors':
                            value_ = recursive_dict_error(indiv)
                        else:
                            value_ = {i: recursive_dict_error(indiv)}
            elif type(copy_of_error[i]) == dict:
                value_ = {i: recursive_dict_error(copy_of_error[i])}
            elif type(copy_of_error[i]) == str:
                value_ = str(i).capitalize().replace("_", " ") + " : " + str(copy_of_error[i])
            elif copy_of_error[i] is None:
                pass
            else:
                raise Exception(type(copy_of_error[i]))
        string_list_objects.append(value_)
        return string_list_objects
    return error


def recursive_list_error(error):
    if type(error) == list:
        return error[0]
    return error


def check_common_member_sets(list_a, list_b):
    set_a = set(list_a)
    set_b = set(list_b)
    return bool(set_a.intersection(set_b))


def mask_private_data(val: str) -> str:
    if not val:
        return ''

    val = str(val)
    length = len(val)

    if length <= 2:
        return val[0] + '*' * (length - 1)
    elif length <= 4:
        return val[0] + '*' * (length - 2) + val[-1]
    else:
        reveal_percent = 0.2 if length > 10 else 0.3
        prefix_len = max(1, int(length * reveal_percent))
        suffix_len = max(1, int(length * reveal_percent))
        masked_len = length - (prefix_len + suffix_len)

        prefix = val[:prefix_len]
        suffix = val[-suffix_len:]
        masked = '*' * masked_len

        return prefix + masked + suffix


def refine_user(user_details):
    if not user_details:
        return False
    if user_details.get('is_refined', False):
        return user_details
    if user_details['usertype'] not in ['PUBLICUSER', 'STAFF', 'PROFESSIONAL', 'COMPANY']:
        return False
    names = ''
    if user_details.get('firstname') not in ['', None]:
        names += user_details['firstname'] + ' '
    else:
        names = user_details.get('name')
    if user_details.get('middlename') not in ['', None]:
        names += user_details['middlename'] + ' '
    if user_details.get('lastname') not in ['', None]:
        names += user_details['lastname']

    res = {
        "user_type": user_details['usertype'],
        "id": user_details['user_id'],
        "names": names,
        "phone_number": user_details['phonenum'],
        "account_number": user_details['account_number'],
        "is_refined": True
    }

    if user_details['usertype'] in ['PUBLICUSER', 'PROFESSIONAL']:
        res["registration_number"] = user_details['id_num']

    elif user_details['usertype'] in ['STAFF']:
        res["registration_number"] = user_details['employeenum']

    else:
        res["registration_number"] = user_details['registration_number']

    return res


def return_foreign_key_ids(data, instance):
    # Iterate over the model fields
    for field in instance._meta.get_fields():
        # Check if the field is a ForeignKey
        if isinstance(field, ForeignKey):
            # Add the foreign key ID to the dictionary
            data[f'{field.name}_id'] = getattr(instance, field.name).id if getattr(instance, field.name) else None

    return data


def recursive_model_to_dict(instance, depth=6):
    """
    Recursively converts a Django model instance into a dictionary,
    including related fields.

    Args:
        instance (Model): The Django model instance to convert.
        depth (int): Controls the depth of recursion for nested relations.

    Returns:
        dict: A dictionary representation of the model instance with related objects.
    """
    if not isinstance(instance, Model):
        return {}  # Return the value if it's not a Django model instance

    # Convert the model instance to a dictionary
    instance_dict = model_to_dict(instance)

    if hasattr(instance, 'id'):
        instance_dict['id'] = instance.id

    if hasattr(instance, 'date_created'):
        instance_dict['date_created'] = instance.date_created

    # Iterate through all related fields of the instance
    for field in instance._meta.get_fields():
        if depth <= 0:  # Stop recursion if the depth limit is reached
            continue

        # Check for related fields (foreign key, one-to-one, many-to-one, many-to-many)
        if field.is_relation and field.name not in instance_dict:
            related_object = getattr(instance, field.name, None)

            if related_object is None:
                instance_dict[field.name] = None
            elif field.one_to_one or field.many_to_one:  # ForeignKey or OneToOneField
                instance_dict[field.name] = recursive_model_to_dict(related_object, depth=depth - 1)
            elif field.one_to_many or field.many_to_many:  # Reverse ForeignKey or ManyToManyField
                related_objects = related_object.all()
                instance_dict[field.name] = [recursive_model_to_dict(obj, depth=depth - 1) for obj in related_objects]

    return instance_dict


server_error = 'A server error occurred processing your request. Contact support.'
request_error = 'Server did not understand your request. Contact support.'


class MakeExternalCall:
	def __init__(self, method, url, headers, params=None, data=None, server_error_500=server_error):
		self.method = method
		self.params = params
		self.data = data
		self.server_error_500 = server_error_500
		self.url = url
		self.headers = headers

	def _return_response_tuple(self, res) -> tuple:
		if res.status_code < 400:
			return True, res.json()
		elif res.status_code == 400:
			print(res.json())
			return False, res.json()['details']
		else:
			logging.error(res.status_code)
			logging.error(res.text)
			return self._return_default_error_response()

	def _run_request_exception(self, func):
		try:
			res = func()
		except requests.exceptions.RequestException as e:
			logging.error(e)
			return self._return_default_error_response()
		return self._return_response_tuple(res)

	def _return_default_error_response(self):
		return False, self.server_error_500

	@staticmethod
	def _return_request_error():
		return False, request_error

	# def _process_request_raise_exception(self):

	def _get_request(self):
		try:
			res = requests.get(url=self.url, params=self.params, headers=self.headers)
		except requests.exceptions.RequestException as e:
			logging.error(e)
			return self._return_request_error()
		return self._return_response_tuple(res)

	def _post_request(self):
		try:
			res = requests.post(url=self.url, json=self.data, headers=self.headers)
		except requests.exceptions.RequestException as e:
			logging.error(f'Url: {self.url}')
			logging.error(e.__traceback__)
			return self._return_request_error()
		return self._return_response_tuple(res)

	def make_api_call(self):
		if self.method.upper() == 'GET':
			return self._get_request()
		if self.method.upper() == 'POST':
			return self._post_request()
		else:
			return False, "Sorry, The server did not understand your request. Try again later"


class SendNotification:
    def __init__(self, headers, process_id, process_name, notification_type="SYSTEM"):
        self.headers = headers
        self.process_name = process_name
        self.process_id = process_id
        self.notification_type = notification_type

    def send_single_notification(self, user_id, _message):
        notification_class = Notification(
            message=_message,
            user_id=str(user_id),
            process=self.process_name,
            task_id=str(self.process_id),
            notification_type=self.notification_type,
            headers=self.headers
        )
        Timer(1, notification_class.send_notification).start()

    def send_bulk_(self, list_of_user_id: list, _message: str):
        data = [
            {
                "message": _message,
                "user_id": str(i),
                "process": self.process_name,
                "notification_type": self.notification_type,
                "task_id": str(self.process_id)
            }
            for i in list_of_user_id
        ]
        notification_class = Notification(
            headers=self.headers,
            data=data
        )
        Timer(1, notification_class.send_bulk_notification).start()


class AssignReassign:
    """This class reassigns users, randomly or by given measure"""
    pass



