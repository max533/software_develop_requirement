""" signature app's api serializers.py """
from rest_framework import serializers


class AccountSerializer(serializers.Serializer):
    """ Account Serializer """
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    code = serializers.CharField(read_only=True)
    business_unit = serializers.CharField(read_only=True)
    project_count = serializers.IntegerField(read_only=True)
