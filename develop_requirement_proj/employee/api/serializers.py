"""employee app's api serializers.py"""
import logging

from develop_requirement_proj.employee.models import Employee

from rest_framework import serializers

logger = logging.getLogger(__name__)


class EmployeeSerializer(serializers.ModelSerializer):
    """ Employee Serializer """

    display_name = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['employee_id', 'extension', 'display_name']

    def get_display_name(self, obj):
        return f'{obj.english_name}/{obj.site}/Wistron'
