"""employee app's api serializers.py"""
import logging

from rest_framework import serializers

from ..models import Employee

logger = logging.getLogger(__name__)


class EmployeeSerializer(serializers.ModelSerializer):
    """Employee Serializer"""

    display_name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['employee_id', 'extension', 'display_name', 'avatar']

    def get_display_name(self, obj):
        return f'{obj.english_name}/{obj.site}/Wistron'

    def get_avatar(self, obj):
        if obj.employee_id not in self.context:
            return None
        return self.context[obj.employee_id]
