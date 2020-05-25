""" signature app's api serializers.py """
from pathlib import Path
from urllib.parse import urlparse, urlunparse

from develop_requirement_proj.employee.api.serializers import (
    EmployeeSerializer,
)

from django.db.models import Max

from rest_framework import serializers

from ..models import Document, ProgressTracker, Schedule


class AccountBaseSerializer(serializers.Serializer):
    """ Account Serializer """
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    code = serializers.CharField(read_only=True)
    business_unit = serializers.IntegerField(read_only=True)


class AccountSerializer(AccountBaseSerializer):
    project_count = serializers.IntegerField(read_only=True)


class ProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    wistron_name = serializers.CharField(read_only=True)
    customer_name = serializers.CharField(read_only=True)
    wistron_code = serializers.CharField(read_only=True)
    plm_code_1 = serializers.CharField(read_only=True)
    plm_code_2 = serializers.CharField(read_only=True)
    deleted_at = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    plm_code = serializers.CharField(read_only=True)
    type = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    product_line = serializers.CharField(read_only=True)
    business_model = serializers.CharField(read_only=True)
    account = AccountBaseSerializer()


class DocumentSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        """ Automatically add file size and uploader """
        validated_data['size'] = self.context['request'].FILES['path'].size
        validated_data['uploader'] = self.context['request'].user.username
        return Document.objects.create(**validated_data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        url = urlparse(ret['path'])
        filepath = str(Path('download') / instance.path.name)
        parts = (url.scheme, url.netloc, filepath, '', '', '')
        ret['path'] = urlunparse(parts)
        return ret

    class Meta:
        model = Document
        fields = "__all__"
        read_only_fields = ['size', 'created_time', 'uploader']


class ScheduleSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        """
        Add automatically same version with current max version schedule.
        If max current version doesn't exist, it will add version value with 1.
        """
        result = Schedule.objects.filter(order=validated_data['order']).aggregate(Max('version'))
        validated_data['version'] = result['version__max'] if result['version__max'] is not None else 1
        return Schedule.objects.create(**validated_data)

    class Meta:
        model = Schedule
        fields = "__all__"
        read_only_fields = ['created_time', 'update_time', 'version']


class ProgressSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['employee'] = self.context['request'].user.username
        return ProgressTracker.objects.create(**validated_data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        employee_id = ret['employee']
        ret['employee'] = self.context['employee'][employee_id]
        return ret

    class Meta:
        model = ProgressTracker
        fields = "__all__"
        read_only_fields = ['employee', 'created_time']


class EmployeeNonModelSerializer(serializers.Serializer):

    employee_id = serializers.CharField()
    display_name = serializers.SerializerMethodField()
    extension = serializers.CharField()
    job_title = serializers.CharField()

    def get_display_name(self, obj):
        return f"{obj['english_name']}/{obj['site']}/Wistron"
