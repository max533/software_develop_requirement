""" develop_requirement_proj API URL Configuration """
from rest_framework_nested import routers

from develop_requirement_proj.employee.api.viewsets import EmployeeViewSet
from develop_requirement_proj.signature.api.viewsets import (
    AccountViewSet, AssignerViewSet, CommentViewSet, DocumentViewSet,
    NotificationVewSet, OptionView, OrderViewSet, ProgressViewSet,
    ProjectViewSet, ScheduleViewSet, SignatureViewSet,
)

from django.conf import settings
from django.urls import path

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

app_name = 'api'

router.register('employees', EmployeeViewSet)
router.register('accounts', AccountViewSet, basename='account')
router.register('projects', ProjectViewSet, basename='project')
router.register('assigners', AssignerViewSet)
router.register('documents', DocumentViewSet)
router.register('schedules', ScheduleViewSet)
router.register('progress', ProgressViewSet, basename='progress')
router.register('comments', CommentViewSet)
router.register('notifications', NotificationVewSet)
router.register('orders', OrderViewSet)
orders_router = routers.NestedDefaultRouter(router, 'orders', lookup='orders')
orders_router.register('signatures', SignatureViewSet, basename='signatures')

urlpatterns = [
    path('options/', OptionView.as_view(), name='option')
]

urlpatterns += router.urls
urlpatterns += orders_router.urls
