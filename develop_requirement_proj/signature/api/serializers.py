""" signature app's api serializers.py """
from pathlib import Path
from urllib.parse import urlparse, urlunparse

from rest_framework import serializers

from ..models import Document


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
