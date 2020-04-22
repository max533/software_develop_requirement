""" signature app's api serializers.py """
from rest_framework import serializers


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
