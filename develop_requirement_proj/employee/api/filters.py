
import logging

from django_filters import rest_framework as filters

from ..models import Employee

logger = logging.getLogger(__name__)


class EmployeeFilter(filters.FilterSet):
    class Meta:
        model = Employee
        fields = {
            'employee_id': ['icontains'],
            'english_name': ['icontains'],
            'department_id': ['icontains'],
            'extension': ['icontains'],
            'site': ['exact'],
        }
