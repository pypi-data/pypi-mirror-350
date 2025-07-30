"""
Preserves generic routers for default views. Just as it happens with auth applications

"""

from rest_framework.routers import DefaultRouter

from ardhi_framework.default_views import RemarksModelViewSet, EventsViewSet

router = DefaultRouter(trailing_slash=False)

router.register('remarks', viewset=RemarksModelViewSet, basename='remarks')
router.register('activity', viewset=EventsViewSet, basename='activity')

urlpatterns = router.urls

