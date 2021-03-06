""" develop_requirement_proj API URL Configuration """
from rest_framework_nested import routers

from develop_requirement_proj.employee.api.viewsets import EmployeeViewSet
from develop_requirement_proj.signature.api.viewsets import (
    CommentViewSet, DocumentViewSet, NotificationVewSet, OptionView,
    OrderViewSet, ProgressViewSet, ScheduleViewSet, SignatureViewSet,
    SystemView,
)

from django.conf import settings
from django.urls import path

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

app_name = 'api'

router.register('employees', EmployeeViewSet)
router.register('documents', DocumentViewSet)
router.register('schedules', ScheduleViewSet)
router.register('progress', ProgressViewSet, basename='progress')
router.register('comments', CommentViewSet)
router.register('notifications', NotificationVewSet)
router.register('orders', OrderViewSet)
orders_router = routers.NestedDefaultRouter(router, 'orders', lookup='orders')
orders_router.register('signatures', SignatureViewSet, basename='signatures')

urlpatterns = [
    path('options/', OptionView.as_view(), name='option'),
    path('systems/', SystemView.as_view(), name='system'),
]

urlpatterns += router.urls
urlpatterns += orders_router.urls
