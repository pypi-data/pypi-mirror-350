import datetime

from django.db import models

from ardhi_framework.exceptions import FraudDetectionError
from ardhi_framework.fields import UserDetailsField, FreezeStateField, ArdhiPrimaryKeyField, ParcelNumberField
from ardhi_framework.interservice import get_user_profile
from ardhi_framework.middleware import get_current_request
from ardhi_framework.utils import decode_jwt, recursive_model_to_dict


class ArdhiModelManager(models.Manager):
    def create(self, **kwargs):
        if 'created_by' not in kwargs:
            actor = ArdhiBaseModel.get_current_actor()
            if actor:
                kwargs['created_by'] = actor
        created_instance = super().create(**kwargs)
        # update_frozen_state_instance(created_instance)
        return created_instance


class ArdhiBaseModel(models.Model):
    id = ArdhiPrimaryKeyField()
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = UserDetailsField()
    last_modified = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    date_deleted = models.DateTimeField(null=True, blank=True)
    deleted_by = UserDetailsField()

    class Meta:
        abstract = True

    objects = ArdhiModelManager()

    def delete(self, using=None, keep_parents=False):
        # no deletion allowed
        raise FraudDetectionError("Action flagged as fraudulent. Deletion not allowed.")

    def update(self, *args, **kwargs):
        # Update and log all information. Freeze in state data
        if kwargs.get('is_deleted'):
            kwargs['deleted_by'] = self.get_current_actor()
            kwargs['date_deleted'] = datetime.datetime.now()

        return super().update(*args, **kwargs)

    @staticmethod
    def get_current_actor():
        request = get_current_request()
        if request:
            user_id = decode_jwt(request.headers.get('JWTAUTH').split(' ')[1])['user']
            return get_user_profile(user_id, request.headers)
        return None


class ArdhiModel(ArdhiBaseModel):
    """
    This model prevents deletion of objects
    Logs all entries, updates, creation, etc
    Every model must have date updated, date created, and last modified
    """
    # readonly field for serializers
    fz = FreezeStateField()

    class Meta:
        abstract = True


def update_frozen_state_instance(instance):
    instance.fz = recursive_model_to_dict(instance)
    instance.save()


class DepartmentParcelRegistryModel(ArdhiModel):
    parcel_number = ParcelNumberField(unique=True)


class EventChangeLogModel(ArdhiModel):
    event_type = models.CharField(max_length=255)
    description = models.TextField()
    data_in = FreezeStateField()
    parcel_number = models.ForeignKey(DepartmentParcelRegistryModel, on_delete=models.SET_NULL, null=True, blank=True,)
    application_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Change Log Activity'
        verbose_name_plural = 'Change Logs Activity'

    def fetch_parcel_number(self):
        return self.parcel_number


class ParcelRelatedDocumentsModel(ArdhiModel):
    """
    This model is used to store generated documents, including uploads, titles, etc
    """
    parcel_number = models.ForeignKey(DepartmentParcelRegistryModel, on_delete=models.SET_NULL, null=True, blank=True,)
    document_id = models.CharField(max_length=255, null=True, blank=True)
    doc_data = FreezeStateField(null=True, blank=True)  # stores doc data especially for on the fly documents



