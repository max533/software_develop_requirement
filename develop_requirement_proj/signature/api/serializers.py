""" signature app's api serializers.py """
import re
from pathlib import Path
from urllib.parse import urlparse, urlunparse

from rest_framework import serializers

from ..models import (
    Comment, Document, Notification, Order, OrderTracker, Progress, Schedule,
    Signature,
)


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
        read_only_fields = ['editor', 'update_time']


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
    schedule = serializers.SerializerMethodField()

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

    def get_schedule(self, obj):
        return self.context['schedules'].get(str(obj.system), [])

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
        Transform system_id to system information.
        And transform employee_id to employee information.
        """
        ret = super().to_representation(instance)

        employees = self.context['employees']
        systems = self.context['systems']
        ret['initiator'] = employees.get(ret['initiator'], ret['initiator'])
        ret['assigner'] = employees.get(ret['assigner'], ret['assigner'])
        try:
            ret['system'] = systems.get(str(ret['system']), ret['system'])[0]
        except Exception:
            ret['system'] = ret['system']

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

    def validate_system(self, value):
        """ Check whether the system_id is in System 2 Online or not """
        if str(value) not in self.context['systems']:
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
