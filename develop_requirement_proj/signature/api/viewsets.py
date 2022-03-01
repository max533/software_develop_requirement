""" signature app's api viewsets.py """
import logging

from develop_requirement_proj.employee.api.serializers import (
    EmployeeSerializer,
)
from develop_requirement_proj.employee.models import Employee
from develop_requirement_proj.utils.exceptions import (
    Conflict, ServiceUnavailable,
)
from develop_requirement_proj.utils.mixins import QueryDataMixin

from django.core.cache import cache
from django.db.models import Max
from django.forms import model_to_dict
from django.utils import timezone

from rest_framework import mixins, response, serializers, views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from ..models import (
    Comment, Document, Notification, Order, Progress, Schedule,
    ScheduleTracker, Signature,
)
from .filters import OrderFilter, OrderFilterBackend
from .mixins import CacheMixin, MessageMixin, SignatureMixin
from .paginations import OrderPagination
from .permissions import (
    CommentPermission, DocumentPermission, NotificationPermission,
    OrderPermission, ProgressPermission, SchedulePermission,
    SignaturePermission,
)
from .serializers import (
    CommentSerializer, DocumentSerializer, NotificationSerializer,
    OrderDynamicSerializer, OrderTrackerSerializer, ProgressSerializer,
    ScheduleSerializer, SignatureSerializer,
)

logger = logging.getLogger(__name__)


class OptionView(QueryDataMixin, views.APIView):
    """ Provide Option resource """

    def get(self, request, *args, **kwargs):
        """ Get result from TeamRoster 2.0 Online, AccPro 2.0 Online and System 2.0 Online """
        options = {}
        params = self.request.query_params.dict()

        if not params:
            raise serializers.ValidationError({"field": "This parameter is required."})
        try:
            options = self.get_option_value(field=params)
        except KeyError as err:
            logger.error(err, exc_info=True)
            raise serializers.ValidationError({"field": "This parameter is required."})
        except ValueError as err:
            logger.error(err, exc_info=True)
            raise serializers.ValidationError({"field": "This value is not reasonable."})
        except Exception as err:
            logger.error(err, exc_info=True)
            raise ServiceUnavailable

        return response.Response(options)


class AssignerViewSet(QueryDataMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """ Provide Assigner resource with `list` action """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        """
        Get queryset from Account Project System and TeamRoster 2.0 System

        1. DQMS assigner is the department manager which is belong to department ( QT + DQMS )

        2. TSC, PM, BMC, BIOS assigner is the department member which is belong to department ( SW + PM )

        3. Other project-based assigner is the department manager of the project owner
        """
        queryset = []
        # Examine the required kwargs information
        kwarg, error = {}, {}
        kwarg['sub_function'] = self.request.query_params.get('sub_function', None)
        kwarg['project_id'] = self.request.query_params.get('project_id', None)
        for key, value in kwarg.items():
            if value is None:
                error.update({key: 'This parameter is required.'})
        if error:
            raise serializers.ValidationError(error)

        params = {'bg': 'EBG'}
        assigner_list = []
        if kwarg['sub_function'] in ['DS']:
            # Use kwarg['sub_function'] to search department id of the assigner
            params['fn_lvl1'] = 'DSPA'
            params['fn_lvl2'] = kwarg['sub_function']
            try:
                departments = self.get_department_via_search(**params)
            except Exception as err:
                logger.error(err, exc_info=True)
                raise ServiceUnavailable

            department_list = departments
            # Use department_id to query employee_id of the department manager
            try:
                departments = self.get_department_via_query(department_list=department_list)
            except Exception as err:
                logger.error(err, exc_info=True)
                raise ServiceUnavailable

            if not departments:
                return Employee.objects.none()

            for department_id, department in departments.items():
                assigner_list.append(department.get('dm', ''))
            # Query the assigner via assigner_list
            queryset.extend(Employee.objects.using('hr').filter(employee_id__in=assigner_list))

        elif kwarg['sub_function'] in ['TSC', 'PM', 'BMC', 'BIOS']:
            # Use kwarg['sub_function'] to search department id of the assigner
            params['fn_lvl1'] = 'SW'
            params['fn_lvl2'] = 'PM'

            try:
                departments = self.get_department_via_search(**params)
            except Exception as err:
                logger.error(err, exc_info=True)
                raise ServiceUnavailable

            # Query the assigner via assigner_dept_list
            queryset.extend(Employee.objects.using('hr').filter(department_id__in=departments))

        else:
            # Use kwarg['sub_function'] and kwarg['project_id'] to get the project leader
            params['fn_lvl2'] = kwarg['sub_function']
            params['projid'] = kwarg['project_id']

            try:
                projects = self.get_project_via_teamroaster_project_search(**params)
            except Exception as err:
                logger.error(err, exc_info=True)
                raise ServiceUnavailable

            if not projects:
                return Employee.objects.none()

            assigner_dept_list = []
            assigner_dept_list.extend([project['lead_dept'] for project in projects])

            # Get the department list of the project leader
            try:
                departments = self.get_department_via_query(department_list=assigner_dept_list)
            except Exception as err:
                logger.error(err, exc_info=True)
                raise ServiceUnavailable

            if not departments:
                return Employee.objects.none()

            for department_id, department in departments.items():
                assigner_list.append(department.get('dm', ''))

            # Query the assigner via asssigner_list
            queryset.extend(Employee.objects.using('hr').filter(employee_id__in=assigner_list))

        return queryset


class DocumentViewSet(viewsets.ModelViewSet):
    """ Provide Document resource with `retrieve`, `list`, `create`, `partial_update` and `delete` """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated & DocumentPermission]

    def get_queryset(self):
        queryset = self.queryset
        order_id = self.request.query_params.get("order", None)
        if order_id is not None:
            queryset = queryset.filter(order=order_id)
        return queryset


class ScheduleViewSet(SignatureMixin, viewsets.ModelViewSet):
    """ Provide Schedule resource with `retrieve`, `list`, `create`, `partial_update` and `delete` """
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated & SchedulePermission]

    def get_queryset(self):
        """ Select queryset depend on which action and filter queryset by order_id """
        queryset = self.queryset

        if self.action in ['group_tracker']:
            queryset = ScheduleTracker.objects.all()

        order_id = self.request.query_params.get('order', None)
        if order_id is None:
            return queryset
        queryset = queryset.filter(order=order_id)

        return queryset

    @action(methods=['GET'], detail=False, url_path='group_tracker', url_name='group-tracker')
    def group_tracker(self, request, *args, **kwargs):
        """ Provide schedule history resource group by version """
        queryset = self.filter_queryset(self.get_queryset())
        data = dict()
        for obj in queryset.values():
            if obj['version'] not in data:
                data[obj['version']] = [obj]
            else:
                data[obj['version']].append(obj)
        return response.Response(data)

    def perform_create(self, serializer):
        serializer.save()
        # If Schedule Add, then Order status rollback to P3 initial status
        order = serializer.instance.order
        # Check whether P4 phase signature is finished or not
        skip_signature_flag, create_new_signature_flag = self.calculate_signature_flag(order.id, 'P4')
        # Order status change
        order.status = {
            'P3': {
                "initiator": "",
                "assigner": "",
                "developers": ""
            },
            'signed': skip_signature_flag
        }
        order.save()
        # Update confirm_status
        schedules = order.schedule_set.all()
        for schedule in schedules:
            schedule.confirm_status = False
        Schedule.objects.bulk_update(schedules, ['confirm_status'])

    def perform_update(self, serializer):
        serializer.save()
        # If Schedule Add, then Order status rollback to P3 initial status
        order = serializer.instance.order
        # Check whether P4 phase signature is finished or not
        skip_signature_flag, create_new_signature_flag = self.calculate_signature_flag(order.id, 'P4')
        # Order status change
        order.status = {
            'P3': {
                "initiator": "",
                "assigner": "",
                "developers": ""
            },
            'signed': skip_signature_flag
        }
        order.save()
        # Update confirm_status
        schedules = order.schedule_set.all()
        for schedule in schedules:
            schedule.confirm_status = False
        Schedule.objects.bulk_update(schedules, ['confirm_status'])

    def perform_destroy(self, instance):
        # If Schedule delete, then Order status rollback to P3 initial status
        order = instance.order
        instance.delete()
        # Check whether P4 phase signature is finished or not
        skip_signature_flag, create_new_signature_flag = self.calculate_signature_flag(order.id, 'P4')
        # Order status change
        order.status = {
            'P3': {
                "initiator": "",
                "assigner": "",
                "developers": ""
            },
            'signed': skip_signature_flag
        }
        order.save()
        # Update confirm_status
        schedules = order.schedule_set.all()
        for schedule in schedules:
            schedule.confirm_status = False
        Schedule.objects.bulk_update(schedules, ['confirm_status'])


class ProgressViewSet(CacheMixin, viewsets.ModelViewSet):
    """ Provide Development Progress Resource with all action. """
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    permission_classes = [IsAuthenticated & ProgressPermission]

    def get_queryset(self):
        """ Filter Development Progress by order_id """
        queryset = self.queryset
        order_id = self.request.query_params.get('order', None)
        if order_id is not None:
            queryset = queryset.filter(order=order_id)
        return queryset

    def get_serializer_context(self):
        """ Provide the employee information to use in to_representation() at serializer.py """
        context = super().get_serializer_context()
        context['employees'] = self.fetch_simple_employees_from_cache()
        return context


class CommentViewSet(CacheMixin, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ Provide Comments resource with `list` and `create` action """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated & CommentPermission]

    def get_queryset(self):
        """ Filter comment by order_id """
        queryset = self.queryset
        order_id = self.request.query_params.get('order', None)
        if order_id is not None:
            queryset = queryset.filter(order=order_id)
        return queryset

    def get_serializer_context(self):
        """ Provide the editor information to use in to_representation() at serializer.py """
        context = super().get_serializer_context()
        context['employees'] = self.fetch_simple_employees_from_cache()
        return context


class NotificationVewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated & NotificationPermission]

    def get_queryset(self):
        """ Get current user's notification """
        queryset = []
        employee_id = self.request.user.username
        queryset = self.queryset.filter(recipient=employee_id)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        unread_count = queryset.filter(read_status=False).count()

        unread_count = unread_count if unread_count is not None else 0

        return response.Response(
            {
                "unread_count": unread_count,
                "data": serializer.data
            }
        )


class OrderViewSet(CacheMixin,
                   MessageMixin,
                   SignatureMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    """ Provide Order Resource with `list`, `retrieve`, `update`, `partial_update`, `create` action """
    queryset = Order.objects.all()
    serializer_class = OrderDynamicSerializer
    pagination_class = OrderPagination
    filter_backends = [OrderFilterBackend]
    filter_class = OrderFilter
    permission_classes = [IsAuthenticated & OrderPermission]

    def get_serializer_context(self):
        """
        Query employee, function_team and sub_function_team information
        for to_represtation() function
        """
        # TODO Use asyncio to speed up the resquest with third-party api
        context = super().get_serializer_context()
        context['employees'] = self.fetch_simple_employees_from_cache()
        context['systems'] = self.get_system_via_search(**{'group': 'id'})
        context['schedules'] = self.get_schedule_via_search(**{'group': 'system_id'})
        # context['schedules'] = dict()
        if self.action in ['create', 'update', 'partial_update']:
            # Get function_team and sub_function information
            function_team_object = cache.get('function_team', None)
            sub_function_team_object = cache.get('sub_function_team', None)

            if function_team_object is None or sub_function_team_object is None:
                function_team_object, sub_function_team_object = [], []

                try:
                    options = self.get_option_value(field={'field': 'dept_category'})
                except Exception as err:
                    logger.error(err, exc_info=True)
                    raise ServiceUnavailable

                if 'EBG' in options:
                    function_team_object = list(options['EBG'].keys())
                    cache.set('function_team', function_team_object, 60 * 60)
                    sub_fun_list = []
                    for key in options['EBG'].keys():
                        sub_fun = options['EBG'][key]
                        sub_fun_list.extend(sub_fun)
                    sub_function_team_object = sub_fun_list
                    cache.set('sub_function_team', sub_function_team_object, 60 * 60)
            context['function_team'] = function_team_object
            context['sub_function_team'] = sub_function_team_object

        return context

    def get_serializer(self, *args, **kwargs):
        """ Add fields(list) into kwargs dict to provide dynamic serializer to use """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        fields = self.request.query_params.get('fields', None)
        if fields:
            kwargs['fields'] = [field for field in fields.split(',')]
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        if self.action == 'history_list':
            serializer_class = OrderTrackerSerializer
        return serializer_class

    def get_paginated_response(self, data):
        """ Adjust the pagination's response to fit bootstrap-table server-side filter """
        assert self.paginator is not None
        return response.Response(
            {
                'rows': data,
                'total': self.paginator.page.paginator.count,
                'totalNotFilter': len(self.queryset),
            }
        )

    @action(methods=['GET'], detail=True, url_path='trackers', url_name='trackers')
    def history_list(self, request, *args, **kwargs):
        """ Get the ancestor list of the order """
        order_instance = self.get_object()
        queryset = order_instance.ordertracker_set.all()
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    @action(methods=['GET'], detail=True, url_path='ancestors', url_name='ancestors')
    def ancestor_list(self, request, *args, **kwargs):
        """ Get the ancestor list of the order """
        order_instance = self.get_object()
        queryset = order_instance.get_ancestors(ascending=True, include_self=True)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(
            initiator=self.request.user.username,
            update_staff=self.request.user.username,
        )

        order_id = serializer.instance.id
        order = Order.objects.get(pk=order_id)
        order_status = order.status

        # Save OrderTracker
        order_tracker_dict = model_to_dict(order)
        order_tracker_dict['form_begin_time'] = order.form_begin_time
        order_tracker_dict['update_time'] = order.update_time
        order_tracker_dict['form_end_time'] = order.form_end_time
        order_tracker_dict['order'] = order.id
        order_tracker_serializer = OrderTrackerSerializer(data=order_tracker_dict)
        if order_tracker_serializer.is_valid(raise_exception=True):
            order_tracker_serializer.save()

        link = f"{self.request.build_absolute_uri(location='/')}?orders={order_id}"
        if 'P0' in order_status:
            direction_flag = order_status['P0'].get('initiator', None)
            if direction_flag == 'Approve':
                skip_signature_flag, create_new_signature_flag = self.calculate_signature_flag(order_id, 'P1')
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}', " +
                    f"skip_signature_flag:'{skip_signature_flag}'"
                )
                logger.debug(debug_message)
                if skip_signature_flag:
                    order.status = {
                        "P2": {
                            "assigner": ""
                        }
                    }
                    order.save()
                    # Send email to assigner
                    self.send_mail_2_single_user(order.assigner, link, category='confirm')
                elif not skip_signature_flag and create_new_signature_flag:
                    # Find next signer
                    next_signer, next_signer_department_id = self.find_next_signer(order_id, signer=order.initiator)
                    # Create Signature
                    signature_next = {
                        'sequence': 1,
                        'signer': next_signer,
                        'sign_unit': next_signer_department_id,
                        'status': '',
                        'comment': '',
                        'role_group': 'initiator',
                        'order': order
                    }
                    Signature.objects.create(**signature_next)
                    # Create default schedule
                    schedule_start = {
                        'event_name': 'Start',
                        'complete_rate': 0,
                        'order': order
                    }
                    schedule_end = {
                        'event_name': 'End',
                        'complete_rate': 100,
                        'order': order
                    }
                    Schedule.objects.create(**schedule_start)
                    Schedule.objects.create(**schedule_end)
                    # Order Status Change
                    order.status = {
                        "P1": {
                            next_signer: ""
                        }
                    }
                    order.save()
                    # Send email to next signer
                    self.send_mail_2_single_user(next_signer, link, category='signing')

                # Send notification to all order attendant
                link = f"{self.request.build_absolute_uri(location='/')}?orders={order_id}"
                category = 'initialization'
                actor = self.request.user.get_english_name()
                verb = 'initialize'
                action_object = 'order'
                self.send_notification(order_id, link, category, actor, verb, action_object)

            elif direction_flag == 'Close':
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}'"
                )
                logger.debug(debug_message)
                order.form_end_time = timezone.now()
                order.save()

    def perform_update(self, serializer):
        serializer.save(
            update_staff=self.request.user.username,
        )
        # P1 and P4 status change in signature api
        order_id = serializer.data['id']
        order = Order.objects.get(pk=order_id)
        order_status = order.status

        # Save OrderTracker
        order_tracker_dict = model_to_dict(order)
        order_tracker_dict['form_begin_time'] = order.form_begin_time
        order_tracker_dict['update_time'] = order.update_time
        order_tracker_dict['form_end_time'] = order.form_end_time
        order_tracker_dict['order'] = order.id
        order_tracker_serializer = OrderTrackerSerializer(data=order_tracker_dict)
        if order_tracker_serializer.is_valid(raise_exception=True):
            order_tracker_serializer.save()

        link = f"{self.request.build_absolute_uri(location='/')}?orders={order_id}"
        if 'P0' in order_status:
            direction_flag = order_status['P0'].get('initiator', None)
            if direction_flag == "Approve":
                skip_signature_flag, create_new_signature_flag = self.calculate_signature_flag(order_id, 'P1')
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}', " +
                    f"skip_signature_flag:'{skip_signature_flag}'"
                )
                logger.debug(debug_message)
                if skip_signature_flag:
                    order.status = {
                        "P2": {
                            "assigner": ""
                        }
                    }
                    order.save()
                    # Send email to assigner
                    self.send_mail_2_single_user(order.assigner, link, category='confirm')
                elif not skip_signature_flag and create_new_signature_flag:
                    # Find next signer
                    next_signer, next_signer_department_id = self.find_next_signer(order_id, signer=order.initiator)
                    # Create next Signature
                    sequence_max = order.signature_set.aggregate(Max('sequence'))['sequence__max']
                    if sequence_max is None:
                        sequence_max = 0
                    next_signature = {
                        'sequence': sequence_max + 1,
                        'signer': next_signer,
                        'sign_unit': next_signer_department_id,
                        'status': '',
                        'comment': '',
                        'role_group': 'initiator',
                        'order': order
                    }
                    Signature.objects.create(**next_signature)
                    # Order Status Change
                    order.status = {
                        "P1": {
                            next_signer: ""
                        }
                    }
                    order.save()
                    # Send email to next signer
                    self.send_mail_2_single_user(next_signer, link, category='signing')
                else:
                    error_message = "This operation is not correct"
                    logger.error(error_message, exc_info=True)
                    raise Conflict

                # Send notification to all order attendant
                category = 'response'
                actor = self.request.user.get_english_name()
                verb = 'approve'
                action_object = 'order'
                self.send_notification(order_id, link, category, actor, verb, action_object)

            elif direction_flag == "Close":
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}'."
                )
                logger.debug(debug_message)
                # Save order close time
                order.form_end_time = timezone.now()
                order.save()
                # Send close order mail to all member
                self.send_mail_2_all(order_id, link, category='close')
                # Send notification to all order attendant
                category = 'response'
                actor = self.request.user.get_english_name()
                verb = 'close'
                action_object = 'order'
                self.send_notification(order_id, link, category, actor, verb, action_object)

        elif 'P2' in order_status:
            direction_flag = order_status['P2'].get('assigner', None)
            if direction_flag == "Approve":
                skip_signature_flag, create_new_signature_flag = self.calculate_signature_flag(order_id, 'P4')
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}', " +
                    f"skip_signature_flag:'{skip_signature_flag}'"
                )
                logger.debug(debug_message)
                # Order status change
                order.status = {
                    "P3": {
                        "initiator": "",
                        "assigner": "",
                        "developers": ""
                    },
                    "signed": skip_signature_flag
                }
                order.save()
                # Send email to assigner
                self.send_mail_2_single_user(order.assigner, link, category='schedule')
                # Send notification to all order attendant
                category = 'response'
                actor = self.request.user.get_english_name()
                verb = 'approve'
                action_object = 'order'
                self.send_notification(order_id, link, category, actor, verb, action_object)

            elif direction_flag == "Return":
                skip_signature_flag, create_new_signature_flag = self.calculate_signature_flag(order_id, 'P1')
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}', " +
                    f"skip_signature_flag:'{skip_signature_flag}'"
                )
                logger.debug(debug_message)
                # Order status change
                order.status = {
                    'P0': {
                        'initiator': ''
                    },
                    'signed': skip_signature_flag
                }
                order.save()
                # Send email to assigner
                self.send_mail_2_single_user(order.initiator, link, category='return')
                # Send notification to all order attendant
                category = 'response'
                actor = self.request.user.get_english_name()
                verb = 'return'
                action_object = 'order'
                self.send_notification(order_id, link, category, actor, verb, action_object)

            elif direction_flag == "Close":
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}'"
                )
                logger.debug(debug_message)
                # Save order close time
                order.form_end_time = timezone.now()
                order.save()
                # Send close order mail to all member
                self.send_mail_2_all(order_id, link, category='close')
                # Send notification to all order attendant
                category = 'response'
                actor = self.request.user.get_english_name()
                verb = 'close'
                action_object = 'order'
                self.send_notification(order_id, link, category, actor, verb, action_object)

        elif 'P3' in order_status:
            status_list = []
            status_list.append(order_status['P3'].get('initiator', None))
            status_list.append(order_status['P3'].get('assigner', None))
            status_list.append(order_status['P3'].get('developers', None))

            if "Return" in status_list:
                direction_flag = "Return"
            elif all(status == "Approve" for status in status_list):
                direction_flag = "Approve"
            elif status_list[1] == "Close":
                direction_flag = "Close"
            elif status_list[1] == "Approve" and status_list[0] == "" and status_list[2] == "":
                direction_flag = "Negotiate"
            else:
                direction_flag = "Wait"

            if direction_flag == "Approve":
                skip_signature_flag, create_new_signature_flag = self.calculate_signature_flag(order_id, 'P4')
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}', " +
                    f"skip_signature_flag:'{skip_signature_flag}'"
                )
                logger.debug(debug_message)
                # Check the all schedule modify or not.
                # If schedule didn't be modified, It will skip below thing.
                # 1. Recalculate the schedule version and record snapshot in ScheduleTracker table
                # 2. Change schedule's all confirm status to True
                objs = order.schedule_set.all()
                if not all(list(objs.values_list('confirm_status', flat=True))):
                    current_max_version = objs.aggregate(Max('version'))['version__max']
                    new_version = 1 if current_max_version is None else current_max_version + 1
                    for obj in objs:
                        obj.version = new_version
                        obj.confirm_status = True
                    Schedule.objects.bulk_update(objs, ['version', 'confirm_status'])
                    sequence_max = ScheduleTracker.objects.aggregate(Max('id'))['id__max']
                    sequence_max = 0 if sequence_max is None else sequence_max
                    for obj in objs:
                        sequence_max += 1
                        obj.id = sequence_max
                    ScheduleTracker.objects.bulk_create(objs)

                if skip_signature_flag:
                    order.status = {
                        "P5": {
                            "developers": ""
                        }
                    }
                    order.save()
                    if 'contactor' in order.developers:
                        self.send_mail_2_single_user(order.developers['contactor'], link, category='confirm')
                elif not skip_signature_flag and create_new_signature_flag:
                    # Find next Singer
                    next_signer, next_signer_department_id = self.find_next_signer(order_id, order.assigner)
                    # Order Status Change
                    order.status = {
                        "P4": {
                            next_signer: ""
                        }
                    }
                    order.save()
                    # Create Signature
                    sequence_max = order.signature_set.aggregate(Max('sequence'))['sequence__max']
                    sequence_new = 1 if sequence_max is None else sequence_max + 1
                    next_signature = {
                        'sequence': sequence_new,
                        'signer': next_signer,
                        'sign_unit': next_signer_department_id,
                        'status': '',
                        'comment': '',
                        'role_group': 'assigner',
                        'order': order
                    }
                    Signature.objects.create(**next_signature)

                    # Send email to next signer
                    self.send_mail_2_single_user(next_signer, link, category='confirm')
                else:
                    pass
                # Send notification to all order attendant
                category = 'negotiation'
                actor = self.request.user.get_english_name()
                verb = 'approve'
                action_object = 'schedule'
                target = 'on order'
                self.send_notification(order_id, link, category, actor, verb, action_object, target)

            elif direction_flag == "Return":
                skip_signature_flag, create_new_signature_flag = self.calculate_signature_flag(order_id, 'P4')
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}', " +
                    f"skip_signature_flag:'{skip_signature_flag}'"
                )
                logger.debug(debug_message)
                # Order status change (keep return value)
                order.status = {
                    "P3": {
                        "initiator": order.status['P3']['initiator'],
                        "assigner": "",
                        "developers": order.status['P3']['developers']
                    },
                    "signed": skip_signature_flag
                }
                order.save()
                # Send email to assigner
                self.send_mail_2_single_user(order.assigner, link, category='reschedule')
                # Send notification to all order attendant
                link = f"{self.request.build_absolute_uri(location='/')}?orders={order_id}"
                category = 'negotiation'
                actor = self.request.user.get_english_name()
                verb = 'return'
                action_object = 'schedule'
                target = 'on order'
                self.send_notification(order_id, link, category, actor, verb, action_object, target)

            elif direction_flag == "Close":
                skip_signature_flag, create_new_signature_flag = self.calculate_signature_flag(order_id, 'P4')
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}', " +
                    f"skip_signature_flag:'{skip_signature_flag}'"
                )
                logger.debug(debug_message)
                # Order Status Change
                order.status = {
                    "P3": {
                        "assigner": "Close",
                    },
                    "signed": skip_signature_flag
                }
                # Save order close time
                order.form_end_time = timezone.now()
                order.save()
                # Send close order mail to all member
                self.send_mail_2_all(order_id, link, category='close')
                # Send notification to all order attendant
                category = 'negotiation'
                actor = self.request.user.get_english_name()
                verb = 'close'
                action_object = 'order'
                self.send_notification(order_id, link, category, actor, verb, action_object)

            elif direction_flag == "Negotiate":
                skip_signature_flag, create_new_signature_flag = self.calculate_signature_flag(order_id, 'P4')
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}', " +
                    f"skip_signature_flag:'{skip_signature_flag}'"
                )
                logger.debug(debug_message)
                # Order Status Change
                order.status = {
                    "P3": {
                        "initiator": "",
                        "assigner": "Approve",
                        "developers": ""
                    },
                    "signed": skip_signature_flag
                }
                order.save()
                # Send mail to initiator and developers contactor
                recipient_employee_id_list = [
                    Employee.objects.using('hr').get(employee_id=order.initiator).employee_id,
                    Employee.objects.using('hr').get(employee_id=order.developers['contactor']).employee_id
                ]
                self.send_mail_2_multiple_user(recipient_employee_id_list, link, 'confirm')
                # Send notification to all order attendant
                category = 'negotiation'
                actor = self.request.user.get_english_name()
                verb = 'approve'
                action_object = 'order'
                self.send_notification(order_id, link, category, actor, verb, action_object)

            elif direction_flag == "Wait":
                skip_signature_flag, create_new_signature_flag = self.calculate_signature_flag(order_id, 'P4')
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}', " +
                    f"skip_signature_flag:'{skip_signature_flag}'"
                )
                logger.debug(debug_message)
                # Order Status Change
                order.status = {
                    "P3": {
                        "initiator": order.status['P3']['initiator'],
                        "assigner": "Approve",
                        "developers": order.status['P3']['developers']
                    },
                    "signed": skip_signature_flag
                }
                order.save()
                # Send notification to all order attendant
                category = 'negotiation'
                actor = self.request.user.get_english_name()
                verb = 'approve'
                action_object = 'schedule'
                target = 'on order'
                self.send_notification(order_id, link, category, actor, verb, action_object, target)

        elif 'P5' in order_status:
            if 'developers' in order_status['P5']:
                direction_flag = order_status['P5'].get('developers', None)
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}'"
                )
                logger.debug(debug_message)
                if direction_flag == "Approve":
                    # Order status change
                    order.status = {
                        "P5": {
                            "initiator": ""
                        }
                    }
                    order.save()
                # Send email to initiator
                self.send_mail_2_single_user(order.initiator, link, category='confirm')
                # Send notification to all order attendant
                category = 'response'
                actor = self.request.user.get_english_name()
                verb = 'approve'
                action_object = 'order'
                self.send_notification(order_id, link, category, actor, verb, action_object)

            elif 'initiator' in order_status['P5']:
                direction_flag = order_status['P5'].get('initiator', None)
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}'"
                )
                logger.debug(debug_message)
                if direction_flag == "Approve":
                    # Order status change
                    order.status = {
                        "P5": {
                            "initiator": "Approve"
                        }
                    }
                    order.save()
                    # Send complete order mail to all member
                    self.send_mail_2_all(order_id, link, category='complete')
                    # Send notification to all order attendant
                    category = 'completion'
                    actor = self.request.user.get_english_name()
                    verb = 'approve'
                    action_object = 'order'
                    self.send_notification(order_id, link, category, actor, verb, action_object)

                elif direction_flag == "Return":
                    # Order status change
                    order.status = {
                        "P5": {
                            "developers": ""
                        }
                    }
                    order.save()
                    # Send mail to all developers
                    recipient_employee_id_list = []
                    if 'contactor' in order.developers:
                        recipient_employee_id_list.append(order.developers['contactor'])
                    if 'member' in order.developers:
                        recipient_employee_id_list.extend(order.developers['member'])
                    self.send_mail_2_multiple_user(recipient_employee_id_list, link, category='return')
                    # Send notification to all order attendant
                    category = 'response'
                    actor = self.request.user.get_english_name()
                    verb = 'return'
                    action_object = 'order'
                    self.send_notification(order_id, link, category, actor, verb, action_object)

                elif direction_flag == "Close":
                    # Order status change
                    order.form_end_time = timezone.now()
                    order.status = {
                        "P5": {
                            "initiator": "Close"
                        }
                    }
                    order.save()
                    # Send close order mail to all member
                    self.send_mail_2_all(order_id, link, category='close')
                    # Send notification to all order attendant
                    category = 'response'
                    actor = self.request.user.get_english_name()
                    verb = 'close'
                    action_object = 'order'
                    self.send_notification(order_id, link, category, actor, verb, action_object)


class SignatureViewSet(CacheMixin,
                       MessageMixin,
                       SignatureMixin,
                       mixins.ListModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    queryset = Signature.objects.all()
    serializer_class = SignatureSerializer
    permission_classes = [IsAuthenticated & SignaturePermission]

    def get_queryset(self):
        queryset = self.queryset.filter(order=self.kwargs['orders_pk'])
        return queryset

    def get_serializer_context(self):
        """
        Query employee information for to_represtation() function
        """
        # TODO Use asyncio to speed up the request with third-party api
        context = super().get_serializer_context()
        # Get employee information
        context['employees'] = self.fetch_simple_employees_from_cache()
        return context

    def perform_update(self, serializer):
        serializer.save(signed_time=timezone.now())
        signature_id = serializer.data['id']
        signature = Signature.objects.get(pk=signature_id)
        direction_flag = signature.status
        order = Order.objects.get(pk=signature.order.id)

        # Save OrderTracker
        order_tracker_dict = model_to_dict(order)
        order_tracker_dict['form_begin_time'] = order.form_begin_time
        order_tracker_dict['update_time'] = order.update_time
        order_tracker_dict['form_end_time'] = order.form_end_time
        order_tracker_dict['order'] = order.id
        order_tracker_serializer = OrderTrackerSerializer(data=order_tracker_dict)
        if order_tracker_serializer.is_valid(raise_exception=True):
            order_tracker_serializer.save()

        link = f"{self.request.build_absolute_uri(location='/')}?orders={order.id}"
        if direction_flag == 'Approve':
            if 'P1' in order.status:
                skip_signature_flag, create_new_signature_flag = self.calculate_signature_flag(order.id, 'P1')
                # Debug Code
                debug_message = (
                    f"Order Status: P1, signature_status:'{direction_flag}', " +
                    f"skip_signature_flag:'{skip_signature_flag}'"
                )
                logger.debug(debug_message)
                if skip_signature_flag:
                    # Order status change
                    order.status = {
                        'P2': {
                            'assigner': ''
                        }
                    }
                    order.save()
                    # Send email to assigner
                    self.send_mail_2_single_user(order.assigner, link, category='confirm')
                elif not skip_signature_flag and create_new_signature_flag:
                    # Find next signer
                    next_signer, next_signer_department_id = self.find_next_signer(order.id, signature.signer)
                    # Order Status Change
                    order.status = {
                        'P1': {
                            next_signer: ''
                        },
                    }
                    order.save()
                    # Create Signature
                    sequence_max = order.signature_set.aggregate(Max('sequence'))['sequence__max']
                    sequence_new = 1 if sequence_max is None else sequence_max + 1
                    next_signature = {
                        'sequence': sequence_new,
                        'signer': next_signer,
                        'sign_unit': next_signer_department_id,
                        'status': '',
                        'comment': '',
                        'role_group': signature.role_group,
                        'order': order
                    }
                    Signature.objects.create(**next_signature)
                    # Send email to next signer
                    self.send_mail_2_single_user(next_signer, link, category='signing')
            elif 'P4' in order.status:
                skip_signature_flag, create_new_signature_flag = self.calculate_signature_flag(order.id, 'P4')
                # Debug Code
                debug_message = (
                    f"Order Phase: P4, signature_status:'{direction_flag}', " +
                    f"skip_signature_flag:'{skip_signature_flag}'"
                )
                logger.debug(debug_message)
                if skip_signature_flag:
                    # Order status change
                    order.status = {
                        'P5': {
                            'developers': ''
                        }
                    }
                    order.save()
                    # Send mail to all developers
                    recipient_employee_id_list = []
                    if 'contactor' in order.developers:
                        recipient_employee_id_list.append(order.developers['contactor'])
                    if 'member' in order.developers:
                        recipient_employee_id_list.extend(order.developers['member'])
                    self.send_mail_2_multiple_user(recipient_employee_id_list, link, category='confirm')
                elif not skip_signature_flag and create_new_signature_flag:
                    # Find next signer
                    next_signer, next_signer_department_id = self.find_next_signer(order.id, signature.signer)
                    # Order Status Change
                    order.status = {
                        'P4': {
                            next_signer: ''
                        },
                    }
                    order.save()
                    # Create Signature
                    sequence_max = order.signature_set.aggregate(Max('sequence'))['sequence__max']
                    sequence_new = 1 if sequence_max is None else sequence_max + 1
                    next_signature = {
                        'sequence': sequence_new,
                        'signer': next_signer,
                        'sign_unit': next_signer_department_id,
                        'status': '',
                        'comment': '',
                        'role_group': signature.role_group,
                        'order': order
                    }
                    Signature.objects.create(**next_signature)
                    # Send email to next signer
                    self.send_mail_2_single_user(next_signer, link, category='signing')
            # Send notification to all order attendant
            category = 'signature'
            actor = self.request.user.get_english_name()
            verb = 'approve'
            action_object = 'order'
            self.send_notification(order.id, link, category, actor, verb, action_object)

        elif direction_flag == 'Return':
            if 'P1' in order.status:
                skip_signature_flag, create_new_signature_flag = self.calculate_signature_flag(order.id, 'P1')
                # Debug Code
                debug_message = (
                    f"Order Phase: P1, signature_status:'{direction_flag}', " +
                    f"skip_signature_flag:'{skip_signature_flag}'"
                )
                # Order status change
                order.status = {
                    'P0': {
                        'initiator': ''
                    },
                    'signed': skip_signature_flag
                }
                order.save()
                # Send mail to initiator
                self.send_mail_2_single_user(order.initiator, link, category='return')
            elif 'P4' in order.status:
                skip_signature_flag, create_new_signature_flag = self.calculate_signature_flag(order.id, 'P4')
                # Debug Code
                debug_message = (
                    f"Order Phase: P4, signature_status:'{direction_flag}', " +
                    f"skip_signature_flag:'{skip_signature_flag}'"
                )
                # Order status change
                order.status = {
                    'P3': {
                        'initiator': '',
                        'assigner': '',
                        'developers': ''
                    },
                    'signed': skip_signature_flag
                }
                order.save()
                # Send mail to assigner
                self.send_mail_2_single_user(order.assigner, link, category='return')

            # Send notification to all order attendant
            category = 'signature'
            actor = self.request.user.get_english_name()
            verb = 'return'
            action_object = 'order'
            self.send_notification(order.id, link, category, actor, verb, action_object)

        elif direction_flag == 'Close':
            if 'P1' in order.status:
                order.status = {
                    'P1': {
                        signature.signer: 'Close'
                    }
                }
                order.form_end_time = timezone.now()
                order.save()
                # Send close order mail to all member
                self.send_mail_2_all(order.id, link, category='close')
            elif 'P4' in order.status:
                # Order status change
                order.status = {
                    'P4': {
                        signature.signer: 'Close'
                    }
                }
                order.form_end_time = timezone.now()
                order.save()
                # Send close order mail to all member
                self.send_mail_2_all(order.id, link, category='close')

            # Send notification to all order attendant
            category = 'signature'
            actor = self.request.user.get_english_name()
            verb = 'close'
            action_object = 'order'
            self.send_notification(order.id, link, category, actor, verb, action_object)


class SystemView(QueryDataMixin, views.APIView):

    def get(self, request, format=None):
        params = self.request.query_params.dict()
        try:
            systems = self.get_system_via_search(**params)
        except Exception as err:
            logger.error(err, exc_info=True)
            raise ServiceUnavailable
        return response.Response(systems)
