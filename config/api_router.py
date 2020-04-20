""" develop_requirement_proj API URL Configuration"""
from develop_requirement_proj.employee.api.viewsets import EmployeeViewSet

from django.conf import settings

from rest_framework import routers

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

app_name = 'api'

router.register('employees', EmployeeViewSet)

urlpatterns = router.urls
