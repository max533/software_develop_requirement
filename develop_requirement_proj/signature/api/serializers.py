""" signature app's api serializers.py """
import re
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
        prefix = Path('download')
        filepath_suffix = '/'.join(Path(url.path).parts[-2::])
        filepath = str(prefix / filepath_suffix)
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
            raise serializers.ValidationError('This is not a reasonable value.')
        return value

    class Meta:
        model = Schedule
        fields = "__all__"
        read_only_fields = [
            'confirm_status',
            'created_time',
            'update_time',
            'version',
        ]


class ProgressSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        """ Automatically add editor """
        validated_data['editor'] = self.context['request'].user.username
        return Progress.objects.create(**validated_data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        employees = self.context['employees']
        ret['editor'] = employees.get(ret['editor'], ret['editor'])
        return ret

    class Meta:
        model = Progress
        fields = "__all__"
        read_only_fields = ['editor', 'udpate_time']


class EmployeeSimpleSerializer(serializers.Serializer):

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
        employees = self.context['employees']
        ret['editor'] = employees.get(ret['editor'], ret['editor'])
        return ret

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ['editor', 'created_time']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = [
            'link',
            'category',
            'recipient',
            'actor',
            'verb',
            'action_object',
            'target',
            'created_time',
            'deleted_time'
        ]


class OrderDynamicSerializer(serializers.ModelSerializer):
    """ Order Serializer with Dynamic Field """
    status_detail = serializers.SerializerMethodField()

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

    def get_status_detail(self, obj):
        employees = self.context['employees']
        for key in obj.status.keys():
            match = re.fullmatch('^P[0-5]$', key)
            if match:
                phase = match.string
                break

        actions = []
        for key, value in obj.status[phase].items():
            action = dict()
            if key in ['initiator', 'assigner']:
                employee_id = getattr(obj, key)
                action.update({'role': key})
                action.update({'response': obj.status[phase][key]})
            elif key == 'developers':
                employee_id = (getattr(obj, key))['contactor']
                action.update({'role': key})
                action.update({'response': obj.status[phase][key]})
            else:
                employee_id = key
                action.update({'role': 'signaturer'})
                action.update({'response': obj.status[phase][employee_id]})

            if employee_id in employees:
                employee = employees.get(employee_id)
            else:
                employee = {'employee_id': employee_id}

            action.update(employee)
            actions.append(action)

        status_detail = {'phase': phase, 'action': actions}

        return status_detail

    def to_representation(self, instance):
        """
        Transform account id & project id to account & project information.
        And transform employee_id to employee information.
        """
        ret = super().to_representation(instance)
        accounts = self.context['accounts']
        employees = self.context['employees']
        projects = self.context['projects']
        ret['account'] = accounts.get(ret['account'], ret['account'])
        ret['initiator'] = employees.get(ret['initiator'], ret['initiator'])
        ret['project'] = projects.get(ret['project'], ret['project'])
        ret['assigner'] = employees.get(ret['assigner'], ret['assigner'])

        developers = ret['developers']

        if 'member' in developers and developers['member']:
            result = []
            member = developers['member']
            for each_member in member:
                result.append(employees.get(each_member, each_member))
            developers['member'] = result
        else:
            developers['member'] = []

        if 'contactor' in developers and developers['contactor']:
            developers['contactor'] = employees.get(developers['contactor'], developers['contactor'])
        else:
            developers['contactor'] = ''

        ret['developers'] = developers

        return ret

    def validate_account(self, value):
        """ Check whether the account is in AccPro 2.0 System or not """
        if value not in self.context['accounts']:
            raise serializers.ValidationError('This is not a reasonable value.')
        return value

    def validate_project(self, value):
        """ Check whether the project is in AccPro 2.0 System or not """
        if value not in self.context['projects']:
            raise serializers.ValidationError('This is not a reasonable value.')
        return value

    def validate_develop_team_function(self, value):
        """ Check whether the develop_team_function is reasonable or not """
        if value not in self.context['function_team']:
            raise serializers.ValidationError('This is not a reasonable value.')
        return value

    def validate_develop_team_sub_function(self, value):
        """ Check whether the develop_team_sub_function is reasonable or not """
        if value not in self.context['sub_function_team']:
            raise serializers.ValidationError('This is not a reasonable value.')
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
                error_message = "There are not such person with developer's contactor field in HR database."
                raise serializers.ValidationError(error_message)

        if 'member' in value and value['member']:
            identity_list = []
            members = value['member']
            for member in members:
                if member not in self.context['employees']:
                    identity_list.append(False)
                else:
                    identity_list.append(True)
            if False in identity_list:
                error_message = "There are not such person with developer's member field in HR database."
                raise serializers.ValidationError(error_message)
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
            raise serializers.ValidationError('This is not a reasonable value.')
        return value

    class Meta:
        model = Order
        exclude = ['lft', 'rght', 'tree_id', 'level']
        read_only_fields = [
            'initiator',
            'form_begin_time',
            'form_end_time',
            'update_time',
            'update_staff',
            'status_detail'
        ]


class ProjectSimpleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class AccountSimpleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    code = serializers.CharField()


class SignatureSerializer(serializers.ModelSerializer):

    def validate_status(self, value):
        if value not in ['Approve', 'Return', 'Close']:
            raise serializers.ValidationError('This is not a reasonable value.')
        if self.instance.status != '':
            raise serializers.ValidationError('This signer has already signed.')
        return value

    def to_representation(self, instance):
        """
        Transform employee_id to employee information.
        """
        ret = super().to_representation(instance)
        employees = self.context['employees']
        ret['signer'] = employees.get(ret['signer'], ret['signer'])
        return ret

    class Meta:
        model = Signature
        fields = "__all__"
        read_only_fields = [
            'sequence',
            'signer',
            'sign_unit',
            'signed_time',
            'role_group',
            'order'
        ]


class OrderTrackerSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = OrderDynamicSerializer(context=self.context).to_representation(instance)
        return ret

    class Meta:
        model = OrderTracker
        fields = "__all__"
