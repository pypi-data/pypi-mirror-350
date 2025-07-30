from rest_framework import serializers

from ardhi_framework.models import EventChangeLogModel, ArdhiModel
from ardhi_framework.utils import mask_private_data, SendNotification


class UserDetailsField(serializers.DictField):
    """
    User details are dynamic. This field masks all private data if the user is not staff or the user is not the actor

    """

    def to_representation(self, value):
        if isinstance(value, dict):
            # masking if not staff and not authorized or current user

            if not self.context['is_staff']:
                if str(self.context['user']) != str(value.get('id', value.get('user_id'))):
                    for k, v in value.items():
                        if k in ['phone_number', 'email', 'krapin', 'registration_number', 'id_num', 'idnum',
                                 'phone_num', 'account_number']:
                            # masks all private data
                            value[k] = mask_private_data(v)
        return value

    def to_internal_value(self, data):
        return data



class RemarksSerializer(serializers.Serializer):
    """
    Serializes remarks for all applications in the system
    """
    remarks = serializers.CharField(max_length=1000)
    actor_details = UserDetailsField()
    actor_role = serializers.CharField(max_length=100)


class EventChangeLogModelSerializer(serializers.ModelSerializer):
    """
    Serializer for the EventChangeLog model.

    This serializer is designed to convert EventChangeLog model instances into
    representations that can be rendered into JSON or other content types. It allows
    for the deserialization of input data to validate and convert it back into
    model instance data. Serializers play a crucial role in Django REST Framework
    to handle transport and storage of data efficiently.

    Attributes
    ----------
    Meta : class
        Inner Meta class where the model to be serialized and fields to be included
        or excluded are defined for use with EventChangeLog.
    """
    class Meta:
        model = EventChangeLogModel
        fields = '__all__'


class BaseApplicationCreateSerializer(serializers.Serializer):
    """
    Base Request create serializer:
        Validates nodes, application availability/validity, and instance for notifications
        Chaecks other conditions as well
    """
    request_id = serializers.UUIDField()

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.validation_errors = []
        self.application_instance: ArdhiModel = None
        self.node_list = []
        self.actor = None
        self.request_status = ["ONGOING"]
        self.other_conditions = []
        self.notification_instance: SendNotification = None
        self.model: ArdhiModel = self.context.get('model')

    def validate(self, attrs):
        super().validate(attrs)
        self.get_application_request(attrs)
        self.check_request_status()
        self.check_all_other_conditions()
        return attrs

    def get_application_request(self, attrs):
        try:
            self.application_instance = self.model.objects.get(id=attrs['request_id'])
        except self.model.DoesNotExist:
            raise serializers.ValidationError('Invalid request received. Try again later')
        self.notification_instance = SendNotification(
            self.context['headers'],
            self.application_instance.id,
            self.application_instance.process_name
        )
        return

    def check_request_status(self):
        if self.application_instance.application_status not in self.request_status:
            raise serializers.ValidationError(
                f'This request cannot be processed at this time. The application request is {self.application_instance.application_status.lower().replace("-", " ")}.')
        if self.application_instance.node not in self.node_list:
            raise serializers.ValidationError('this request cannot be processed at this stage. Try again later')
        return

    def check_all_other_conditions(self):
        for condition in self.other_conditions:
            if not condition['condition']:
                raise serializers.ValidationError(condition['message'])
        return


