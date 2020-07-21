""" signature app's api serializers.py """
from pathlib import Path
from urllib.parse import urlparse, urlunparse

from rest_framework import serializers

from ..models import (
    Comment, Document, Notification, Order, OrderTracker, Progress, Schedule,
    Signature,
)


class AccountBaseSerializer(serializers.Serializer):
    """ Account Base Serializer """
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    code = serializers.CharField(read_only=True)
    business_unit = serializers.IntegerField(read_only=True)


class AccountSerializer(AccountBaseSerializer):
    """ Account Serializer """
    project_count = serializers.IntegerField(read_only=True)


class ProjectSerializer(serializers.Serializer):
    """ Project Serializer """
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
        read_only_fields = ['size', 'update_time', 'uploader']


class ScheduleSerializer(serializers.ModelSerializer):

    def validate_complete_rate(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError('This is not a reasonable value')
        return value

    class Meta:
        model = Schedule
        fields = "__all__"
        read_only_fields = ['created_time', 'update_time', 'version', 'confirm_status']


class ProgressSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        """ Automatically add editor """
        validated_data['editor'] = self.context['request'].user.username
        return Progress.objects.create(**validated_data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        employee_id = ret['editor']
        ret['editor'] = self.context['employees'][employee_id]
        return ret

    class Meta:
        model = Progress
        fields = "__all__"
        read_only_fields = ['editor', 'udpate_time']


class EmployeeNonModelSerializer(serializers.Serializer):

    employee_id = serializers.CharField()
    display_name = serializers.SerializerMethodField()
    extension = serializers.CharField()
    job_title = serializers.CharField()

    def get_display_name(self, obj):
        return f"{obj['english_name']}/{obj['site']}/Wistron"


class CommentSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        """ Automatically add editor """
        validated_data['editor'] = self.context['request'].user.username
        return Comment.objects.create(**validated_data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        employee_id = ret['editor']
        ret['editor'] = self.context['employees'][employee_id]
        return ret

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ['editor', 'created_time']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ['link', 'category', 'initiator', 'created_time', 'owner']


class OrderDynamicSerializer(serializers.ModelSerializer):
    """ Order Serializer with Dynamic Field """
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(OrderDynamicSerializer, self).__init__(*args, **kwargs)

        # Dynamically generate serializer field
        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def to_representation(self, instance):
        """
        Transform account id & project id to account & project information.
        And transform emeployee_id to employee information.
        """
        ret = super().to_representation(instance)
        if 'account' in ret:
            ret['account'] = self.context['accounts'].get(ret['account'], '')

        if 'initiator' in ret:
            ret['initiator'] = self.context['employees'].get(ret['initiator'], '')

        if 'project' in ret:
            ret['project'] = self.context['projects'].get(ret['project'], '')

        if 'assigner' in ret:
            ret['assigner'] = self.context['employees'].get(ret['assigner'], '')

        if 'developers' in ret:
            if 'member' in ret['developers']:
                member = ret['developers']['member']
                if member:
                    result = []
                    # Jsonfield will encounter some problem in serializer and it will keep convert data in html render
                    # The browser show error message that it will not convert data again after converting
                    # We use data type to check whether convert data or not
                    first_member = member[0]
                    if type(first_member) == str:
                        for each_member in member:
                            result.append(self.context['employees'].get(each_member, ''))
                        ret['developers']['member'] = result
                else:
                    ret['developers']['member'] = []
            else:
                ret['developers']['member'] = []
            if 'contactor' in ret['developers']:
                if type(ret['developers']['contactor']) == str:
                    ret['developers']['contactor'] = self.context['employees'].get(ret['developers']['contactor'], '')
            else:
                ret['developers']['contactor'] = ''

        return ret

    def validate_account(self, value):
        """ Check whether the account is in AccPro 2.0 System or not """
        if value not in self.context['accounts']:
            raise serializers.ValidationError('The account is not reasonable value')
        return value

    def validate_project(self, value):
        """ Check whether the project is in AccPro 2.0 System or not """
        if value not in self.context['projects']:
            raise serializers.ValidationError('The project is not reasonable value')
        return value

    def validate_develop_team_function(self, value):
        """ Check whether the develop_team_function is reasonable or not """
        if value not in self.context['function_team']:
            raise serializers.ValidationError('The develop_team_function is not reasonable value')
        return value

    def validate_develop_team_sub_function(self, value):
        """ Check whether the develop_team_sub_function is reasonable or not """
        if value not in self.context['sub_function_team']:
            raise serializers.ValidationError('The develop_team_sub_function is not reasonable value')
        return value

    def validate_assigner(self, value):
        """ Check whether the assigner in the EBG HR database or not """
        if not (value in self.context['employees']):
            raise serializers.ValidationError('There are not such person.')
        return value

    def validate_developers(self, value):
        """ Check whether the developers in the EBG HR database or not """
        if 'contactor' not in value:
            raise serializers.ValidationError('There are not contactor in developers.')
        else:
            if value['contactor'] not in self.context['employees']:
                raise serializers.ValidationError('There are not such person.')

        if 'member' in value:
            identity_list = []
            members = value['member']
            if members:
                for member in members:
                    if member not in self.context['employees']:
                        identity_list.append(False)
                    else:
                        identity_list.append(True)
                if False in identity_list:
                    raise serializers.ValidationError('There are not such person.')
        return value

    def validate_status(self, value):
        """ Check the status is reasonable or not """
        status_list = [
            {
                "P0": {"initiator": "Close"},
                "signed": True
            },
            {
                "P0": {"initiator": "Close"},
                "signed": False
            },
            {
                "P0": {"initiator": "Approve"},
                "signed": True
            },
            {
                "P0": {"initiator": "Approve"},
                "signed": False
            },
            {"P2": {"assigner": "Approve"}},
            {"P2": {"assigner": "Return"}},
            {"P2": {"assigner": "Close"}},
            {
                "P3": {
                    "assigner": "Close",
                },
                "signed": True,
            },
            {
                "P3": {
                    "assigner": "Close",
                },
                "signed": False,
            },
            {
                "P3": {
                    "initiator": "",
                    "assigner": "",
                    "developers": "",
                },
                "signed": True,
            },
            {
                "P3": {
                    "initiator": "",
                    "assigner": "",
                    "developers": "",
                },
                "signed": False,
            },
            {
                "P3": {
                    "initiator": "",
                    "assigner": "Close",
                    "developers": "",
                },
                "signed": True,
            },
            {
                "P3": {
                    "initiator": "",
                    "assigner": "Close",
                    "developers": "",
                },
                "signed": False,
            },
            {
                "P3": {
                    "initiator": "",
                    "assigner": "Approve",
                    "developers": "",
                },
                "signed": True,
            },
            {
                "P3": {
                    "initiator": "",
                    "assigner": "Approve",
                    "developers": "",
                },
                "signed": False,
            },
            {
                "P3": {
                    "initiator": "Return",
                    "assigner": "Approve",
                    "developers": "",
                },
                "signed": True,
            },
            {
                "P3": {
                    "initiator": "Return",
                    "assigner": "Approve",
                    "developers": "",
                },
                "signed": False,
            },
            {
                "P3": {
                    "initiator": "",
                    "assigner": "Approve",
                    "developers": "Return",
                },
                "signed": True,
            },
            {
                "P3": {
                    "initiator": "",
                    "assigner": "Approve",
                    "developers": "Return",
                },
                "signed": False,
            },
            {
                "P3": {
                    "initiator": "Approve",
                    "assigner": "Approve",
                    "developers": "",
                },
                "signed": True,
            },
            {
                "P3": {
                    "initiator": "Approve",
                    "assigner": "Approve",
                    "developers": "",
                },
                "signed": False,
            },
            {
                "P3": {
                    "initiator": "Approve",
                    "assigner": "Approve",
                    "developers": "Return",
                },
                "signed": True,
            },
            {
                "P3": {
                    "initiator": "Approve",
                    "assigner": "Approve",
                    "developers": "Return",
                },
                "signed": False,
            },
            {
                "P3": {
                    "initiator": "",
                    "assigner": "Approve",
                    "developers": "Approve",
                },
                "signed": True,
            },
            {
                "P3": {
                    "initiator": "",
                    "assigner": "Approve",
                    "developers": "Approve",
                },
                "signed": False,
            },
            {
                "P3": {
                    "initiator": "Return",
                    "assigner": "Approve",
                    "developers": "Approve",
                },
                "signed": True,
            },
            {
                "P3": {
                    "initiator": "Return",
                    "assigner": "Approve",
                    "developers": "Approve",
                },
                "signed": False,
            },
            {
                "P3": {
                    "initiator": "Approve",
                    "assigner": "Approve",
                    "developers": "Approve",
                },
                "signed": True,
            },
            {
                "P3": {
                    "initiator": "Approve",
                    "assigner": "Approve",
                    "developers": "Approve",
                },
                "signed": False,
            },
            {"P5": {"developers": "Approve"}},
            {"P5": {"initiator": "Return"}},
            {"P5": {"initiator": "Approve"}},
            {"P5": {"initiator": "Close"}},
        ]
        if value not in status_list:
            raise serializers.ValidationError('The status is not reasonable value')
        return value

    class Meta:
        model = Order
        exclude = ['lft', 'rght', 'tree_id', 'level']
        read_only_fields = [
            'initiator',
            'form_begin_time',
            'form_end_time',
            'update_time',
            'update_staff'
        ]


class ProjectEasySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class AccountEasySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    code = serializers.CharField()


class SignatureSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        """
        Transform emeployee_id to employee information.
        """
        ret = super().to_representation(instance)

        if 'signer' in ret:
            ret['signer'] = self.context['employees'].get(ret['signer'], '')

        return ret

    class Meta:
        model = Signature
        fields = "__all__"
        read_only_fields = ['sequence', 'signer', 'sign_unit', 'signed_time', 'role_group', 'order']


class OrderTrackerSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderTracker
        fields = "__all__"
        read_only_fields = ['form_begin_time', 'form_end_time', 'order']
