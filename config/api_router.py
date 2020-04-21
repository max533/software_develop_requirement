""" develop_requirement_proj API URL Configuration """
from develop_requirement_proj.employee.api.viewsets import EmployeeViewSet
from develop_requirement_proj.signature.api.viewsets import AccountViewSet

from django.conf import settings

from rest_framework import routers

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

app_name = 'api'

router.register('employees', EmployeeViewSet)
router.register('accounts', AccountViewSet, basename='account')

urlpatterns = router.urls
