""" develop_requirement_proj API URL Configuration """
from develop_requirement_proj.employee.api.viewsets import EmployeeViewSet
from develop_requirement_proj.signature.api.viewsets import (
    AccountViewSet, AssginerViewSet, DocumentViewSet, HistoryViewSet,
    OptionView, ProgressViewSet, ProjectViewSet, ScheduleViewSet,
)

from django.conf import settings
from django.urls import path

from rest_framework import routers

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

app_name = 'api'

router.register('employees', EmployeeViewSet)
router.register('accounts', AccountViewSet, basename='account')
router.register('projects', ProjectViewSet, basename='project')
router.register('assigners', AssginerViewSet)
router.register('documents', DocumentViewSet)
router.register('schedules', ScheduleViewSet)
router.register('progress', ProgressViewSet, basename='progress')
router.register('histories', HistoryViewSet)

urlpatterns = [
    path('options/', OptionView.as_view(), name='option')
]

urlpatterns += router.urls
