"""
For consolidated functions, this will provide basic views for common actions
Now: the command to start a service or an application will generate base views, but generally.
However, each application will be required to define its own parameters for views
"""

from ardhi_framework.generics import ArdhiModelViewSet
from ardhi_framework.models import ArdhiBaseModel, EventChangeLogModel, DepartmentParcelRegistryModel
from ardhi_framework.serializers import RemarksSerializer, EventChangeLogModelSerializer
from django.apps import apps


class EventsViewSet(ArdhiModelViewSet):
    model = EventChangeLogModel
    serializer_class = EventChangeLogModelSerializer
    queryset = model.objects.all()
    searched_fields = ['actor_role', 'actor_details__user_id', 'event_type', 'parcel_number']

    def perform_create(self, serializer):
        """An event cannot be created from external sources"""
        return

    def perform_update(self, serializer):
        """An event cannot be updated once added"""
        return


class ParcelNumberHistory(ArdhiModelViewSet):
    model = DepartmentParcelRegistryModel
    serializer_class = None
    queryset = model.objects.all()
    searched_fields = ['parcel_number', ]

    def perform_create(self, serializer):
        """An event cannot be created from external sources"""
        return

    def perform_update(self, serializer):
        """An event cannot be updated once added"""
        return


class RemarksModelViewSet(ArdhiModelViewSet):
    """
    Remarks model for general remarks
    """

    try:
        model: ArdhiBaseModel = apps.get_model('remarks.RemarksModel')
    except LookupError:
        model = ArdhiBaseModel

    serializer_class = RemarksSerializer
    queryset = model.objects.all()

    def perform_update(self, serializer):
        """Remarks cannot be updated once added"""
        return








