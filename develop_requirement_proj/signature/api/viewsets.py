""" singature app's api viewsets.py """
import logging

from develop_requirement_proj.employee.api.serializers import (
    EmployeeSerializer,
)
from develop_requirement_proj.employee.models import Employee
from develop_requirement_proj.utils.exceptions import Conflict
from develop_requirement_proj.utils.mixins import (
    MessageMixin, QueryDataMixin, SignatureMixin,
)

from django.core.cache import cache
from django.db.models import Max
from django.forms import model_to_dict
from django.utils import timezone

from rest_framework import mixins, response, serializers, views, viewsets
from rest_framework.decorators import action

from ..models import (
    Account, Comment, Document, Notification, Order, Progress, Project,
    Schedule, ScheduleTracker, Signature,
)
from .filters import OrderFilter, OrderFilterBackend
from .paginations import OrderPagination
from .serializers import (
    AccountEasySerializer, AccountSerializer, CommentSerializer,
    DocumentSerializer, EmployeeNonModelSerializer, NotificationSerializer,
    OrderDynamicSerializer, OrderTrackerSerializer, ProgressSerializer,
    ProjectEasySerializer, ProjectSerializer, ScheduleSerializer,
    SignatureSerializer,
)

logger = logging.getLogger(__name__)


class AccountViewSet(QueryDataMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """ Provide Account resource with `list` action """
    serializer_class = AccountSerializer

    def get_queryset(self):
        """ Get queryset from Account Project System """
        queryset = []
        status, results = self.get_account_via_search()
        if status and results:
            queryset = [Account(**result) for result in results]

        return queryset


class ProjectViewSet(QueryDataMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """ Provide Project resource with `list` action """
    serializer_class = ProjectSerializer

    def get_queryset(self):
        """ Get queryset from Account Project System """
        queryset = []
        params = self.request.query_params.dict()
        status, results = self.get_project_via_search(**params)
        if status and results:
            queryset = [Project(**result) for result in results]

        return queryset


class OptionView(QueryDataMixin, views.APIView):
    """ Provide Option resource """

    def get(self, request, *args, **kwargs):
        """ Get result from TeamRoster 2.0 System and Account Project System """
        final_result = {}
        params = self.request.query_params.dict()
        status, result = self.get_option_value(**params)
        if status and result:
            final_result = result

        return response.Response(final_result)


class AssginerViewSet(QueryDataMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """ Provide Assigner resource with `list` action """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        """
        Get queryset from Account Project System and TeamRoster 2.0 System

        1. DQMS assigner is the deaprtment manager which is belong to department ( QT + DQMS )

        2. TSC, PM, BMC, BIOS assigner is the deaprtment member which is belong to department ( SW + PM )

        3. Other project-based assigner is the deparment manager of the project owner
        """
        queryset = []
        # Exanmie the required kwargs information
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
        if kwarg['sub_function'] in ['DQMS']:
            # Use kwarg['sub_function'] to search department id of the assigner
            params['fn_lvl1'] = 'QT'
            params['fn_lvl2'] = kwarg['sub_function']
            status, results = self.get_department_via_search(**params)
            if not (status and results):
                return queryset
            department_id = results[0]
            # Use department_id to query employee_id of the department manager
            status, results = self.get_department_via_query(department_id=department_id)
            if not (status and results):
                return queryset
            for result in results:
                assigner_list.append(results[department_id]['dm'])
            # Query the assigner via assigner_list
            queryset.extend(Employee.objects.using('hr').filter(employee_id__in=assigner_list))

        elif kwarg['sub_function'] in ['TSC', 'PM', 'BMC', 'BIOS']:
            # Use kwarg['sub_function'] to search department id of the assigner
            params['fn_lvl1'] = 'SW'
            params['fn_lvl2'] = 'PM'
            status, results = self.get_department_via_search(**params)
            if not (status and results):
                return queryset
            assigner_dept_list = [result for result in results]
            # Query the assigner via assigner_dept_list
            queryset.extend(Employee.objects.using('hr').filter(department_id__in=assigner_dept_list))

        else:
            # Use kwarg['sub_function'] and kwarg['project_id'] to get the project leader
            params['fn_lvl2'] = kwarg['sub_function']
            params['projid'] = kwarg['project_id']
            status, results = self.get_project_via_teamroaster_project_serach(**params)
            if not (status and results):
                return queryset
            assigner_dept_list = [result.get('lead_dept', '') for result in results]
            # Get the department list of the project leader
            status, results = self.get_department_via_query(*assigner_dept_list)
            if not (status and results):
                return queryset
            for key, value in results.items():
                assigner_list.append(value.get('dm', ''))
            # Query the assigner via asssigner_list
            queryset.extend(Employee.objects.using('hr').filter(employee_id__in=assigner_list))

        return queryset


class DocumentViewSet(viewsets.ModelViewSet):
    """ Provide Document resource with `retrieve`, `list`, `create`, `partial_update` and `delete` """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

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
        result = dict()
        for obj in queryset.values():
            if obj['version'] not in result:
                result[obj['version']] = [obj]
            else:
                result[obj['version']].append(obj)
        return response.Response(result)

    def perform_create(self, serializer):
        serializer.save()
        # If Schedule Add, then Order status rollback to P3 initial status
        order = serializer.instance.order
        # Check whether P4 phase signature is finished or not
        skip_signature_flag, create_new_signaure_flag = self.calculate_signature_flag(order.id, 'P4')
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
        skip_signature_flag, create_new_signaure_flag = self.calculate_signature_flag(order.id, 'P4')
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
        skip_signature_flag, create_new_signaure_flag = self.calculate_signature_flag(order.id, 'P4')
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


class ProgressViewSet(viewsets.ModelViewSet):
    """ Provide Development Progress Resource with all action. """
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer

    def get_queryset(self):
        """ Filter Development Progress by order_id """
        queryset = self.queryset
        order_id = self.request.query_params.get('order', None)
        if order_id is not None:
            queryset = queryset.filter(order=order_id)
        return queryset

    def get_serializer_context(self):
        """ Provide the employee inforamtion to use in to_representation() at serializer.py """
        context = super().get_serializer_context()
        objects = cache.get('employees')
        if objects is None:
            instance = Employee.objects.using('hr').all().values()
            serializer = EmployeeNonModelSerializer(instance, many=True)

            objects = {}
            for employee in serializer.data:
                employee_id = employee['employee_id']
                if employee_id not in objects:
                    objects[employee_id] = employee
            cache.set('employees', objects, 60 * 60)
        context['employees'] = objects
        return context


class CommentViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ Provide Comments resource with `list` and `create` action """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        """ Filter comment by order_id """
        queryset = self.queryset
        order_id = self.request.query_params.get('order', None)
        if order_id is not None:
            queryset = queryset.filter(order=order_id)
        return queryset

    def get_serializer_context(self):
        """ Provide the editor inforamtion to use in to_representation() at serializer.py """
        context = super().get_serializer_context()
        objects = cache.get('employees')
        if objects is None:
            instance = Employee.objects.using('hr').all().values()
            serializer = EmployeeNonModelSerializer(instance, many=True)

            objects = {}
            for employee in serializer.data:
                employee_id = employee['employee_id']
                if employee_id not in objects:
                    objects[employee_id] = employee
            cache.set('employees', objects, 60 * 60)
        context['employees'] = objects
        return context


class NotificationVewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        """ Get current user's notification """
        queryset = []
        employee_id = self.request.user.username
        queryset = self.queryset.filter(recipient=employee_id)
        return queryset


class OrderViewSet(MessageMixin,
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

    def get_serializer_context(self):
        """
        Query account, acccount, employee, function_team and sub_function_team information
        for to_represtation() function
        """
        # TODO Use asyncio to speed up the reuqest with third-party api
        context = super().get_serializer_context()

        # Get project information
        project_object = cache.get('projects', None)
        if project_object is None:
            project_object = {}
            status, results = self.get_project_via_search()

            if status and results:
                serializer = ProjectEasySerializer(results, many=True)
                for project in serializer.data:
                    project_id = project['id']
                    if project_id not in project_object:
                        project_object[project_id] = project
                cache.set('projects', project_object, 60 * 60)
        context['projects'] = project_object

        # Get account information
        account_object = cache.get('accounts', None)
        if account_object is None:
            account_object = {}
            status, results = self.get_account_via_search()

            if status and results:
                serializer = AccountEasySerializer(results, many=True)
                for account in serializer.data:
                    account_id = account['id']
                    if account_id not in account_object:
                        account_object[account_id] = account
                cache.set('accounts', account_object, 60 * 60)
        context['accounts'] = account_object

        # Get employee information
        employee_object = cache.get('employees', None)
        if employee_object is None:
            instance = Employee.objects.using('hr').all().values()
            serializer = EmployeeNonModelSerializer(instance, many=True)

            employee_object = {}
            for employee in serializer.data:
                employee_id = employee['employee_id']
                if employee_id not in employee_object:
                    employee_object[employee_id] = employee
            cache.set('employees', employee_object, 60 * 60)
        context['employees'] = employee_object

        if self.action in ['create', 'update', 'partial_update']:
            # Get function_team and sub_function information
            function_team_object = cache.get('function_team', None)
            sub_function_team_object = cache.get('sub_function_team', None)

            if function_team_object is None or sub_function_team_object is None:
                function_team_object, sub_function_team_object = [], []

                status, result = self.get_option_value(**{'field': 'dept_category'})

                if status and result:
                    if 'EBG' in result:
                        function_team_object = list(result['EBG'].keys())
                        cache.set('function_team', function_team_object, 60 * 60)
                        sub_fun_list = []
                        for key in result['EBG'].keys():
                            sub_fun = result['EBG'][key]
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
        order_tracker_serializer = OrderTrackerSerializer(data=model_to_dict(order))
        if order_tracker_serializer.is_valid(raise_exception=True):
            order_tracker_serializer.save(
                order=order,
                form_begin_time=order.form_begin_time,
                form_end_time=order.form_end_time,
                update_time=order.update_time
            )

        link = f"{self.request.build_absolute_uri(location='/')}?order={order_id}"
        if 'P0' in order_status:
            direction_flag = order_status['P0'].get('initiator', None)
            if direction_flag == 'Approve':
                skip_signature_flag, create_new_signaure_flag = self.calculate_signature_flag(order_id, 'P1')
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}', " +
                    f"skip_signature_flag:'{skip_signature_flag}'"
                )
                logger.debug(debug_message)
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

                # Send notification to all order attendent
                link = f"{self.request.build_absolute_uri(location='/')}?order={order_id}"
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
        order_tracker_serializer = OrderTrackerSerializer(data=model_to_dict(order))
        if order_tracker_serializer.is_valid(raise_exception=True):
            order_tracker_serializer.save(
                order=order,
                form_begin_time=order.form_begin_time,
                form_end_time=order.form_end_time,
                update_time=order.update_time
            )

        link = f"{self.request.build_absolute_uri(location='/')}?order={order_id}"
        if 'P0' in order_status:
            direction_flag = order_status['P0'].get('initiator', None)
            if direction_flag == "Approve":
                skip_signature_flag, create_new_signaure_flag = self.calculate_signature_flag(order_id, 'P1')
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
                elif not skip_signature_flag and create_new_signaure_flag:
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
                    logger.error(error_message)
                    raise Conflict

                # Send notification to all order attendent
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
                # Send notification to all order attendent
                category = 'response'
                actor = self.request.user.get_english_name()
                verb = 'close'
                action_object = 'order'
                self.send_notification(order_id, link, category, actor, verb, action_object)

        elif 'P2' in order_status:
            direction_flag = order_status['P2'].get('assigner', None)
            if direction_flag == "Approve":
                skip_signature_flag, create_new_signaure_flag = self.calculate_signature_flag(order_id, 'P4')
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
                # Send notification to all order attendent
                category = 'response'
                actor = self.request.user.get_english_name()
                verb = 'approve'
                action_object = 'order'
                self.send_notification(order_id, link, category, actor, verb, action_object)

            elif direction_flag == "Return":
                skip_signature_flag, create_new_signaure_flag = self.calculate_signature_flag(order_id, 'P1')
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
                # Send notification to all order attendent
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
                # Send notification to all order attendent
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
                skip_signature_flag, create_new_signaure_flag = self.calculate_signature_flag(order_id, 'P4')
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}', " +
                    f"skip_signature_flag:'{skip_signature_flag}'"
                )
                logger.debug(debug_message)
                # Check the all schedule modify or not.
                # If schedule didn't be modified, It will skip bleow thing.
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
                    result = ScheduleTracker.objects.aggregate(Max('id'))['id__max']
                    new_id = 0 if result is None else result
                    for obj in objs:
                        new_id += 1
                        obj.id = new_id
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
                elif not skip_signature_flag and create_new_signaure_flag:
                    # Find next Singer
                    next_signer, next_signer_department_id = self.find_next_signer(order_id, order.assigner)
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
                    # Order Status Change
                    order.status = {
                        "P4": {
                            next_signer: ""
                        }
                    }
                    order.save()
                    # Send email to next signer
                    self.send_mail_2_single_user(next_signer, link, category='confirm')
                else:
                    pass
                # Send notification to all order attendent
                category = 'negotiation'
                actor = self.request.user.get_english_name()
                verb = 'approve'
                action_object = 'schedule'
                target = 'on order'
                self.send_notification(order_id, link, category, actor, verb, action_object, target)

            elif direction_flag == "Return":
                skip_signature_flag, create_new_signaure_flag = self.calculate_signature_flag(order_id, 'P4')
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
                # Send notification to all order attendent
                link = f"{self.request.build_absolute_uri(location='/')}?order={order_id}"
                category = 'negotiation'
                actor = self.request.user.get_english_name()
                verb = 'return'
                action_object = 'schedule'
                target = 'on order'
                self.send_notification(order_id, link, category, actor, verb, action_object, target)

            elif direction_flag == "Close":
                skip_signature_flag, create_new_signaure_flag = self.calculate_signature_flag(order_id, 'P4')
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}', " +
                    f"skip_signature_flag:'{skip_signature_flag}'"
                )
                logger.debug(debug_message)
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
                # Send notification to all order attendent
                category = 'negotiation'
                actor = self.request.user.get_english_name()
                verb = 'close'
                action_object = 'order'
                self.send_notification(order_id, link, category, actor, verb, action_object)

            elif direction_flag == "Negotiate":
                skip_signature_flag, create_new_signaure_flag = self.calculate_signature_flag(order_id, 'P4')
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}', " +
                    f"skip_signature_flag:'{skip_signature_flag}'"
                )
                logger.debug(debug_message)
                # Send mail to initiator and developers contactor
                recipient_employee_id_list = [
                    Employee.objects.using('hr').get(employee_id=order.initiator).employee_id,
                    Employee.objects.using('hr').get(employee_id=order.developers['contactor']).employee_id
                ]
                self.send_mail_2_multiple_user(recipient_employee_id_list, link, 'confirm')
                # Send notification to all order attendent
                category = 'negotiation'
                actor = self.request.user.get_english_name()
                verb = 'approve'
                action_object = 'order'
                self.send_notification(order_id, link, category, actor, verb, action_object)

            elif direction_flag == "Wait":
                skip_signature_flag, create_new_signaure_flag = self.calculate_signature_flag(order_id, 'P4')
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}', " +
                    f"skip_signature_flag:'{skip_signature_flag}'"
                )
                logger.debug(debug_message)
                # Send notification to all order attendent
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
                # Send notification to all order attendent
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
                    # Send complete order mail to all member
                    self.send_mail_2_all(order_id, link, category='complete')
                    # Send notification to all order attendent
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
                    # Send notification to all order attendent
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
                    # Send notification to all order attendent
                    category = 'response'
                    actor = self.request.user.get_english_name()
                    verb = 'close'
                    action_object = 'order'
                    self.send_notification(order_id, link, category, actor, verb, action_object)


class SignatureViewSet(MessageMixin,
                       SignatureMixin,
                       mixins.ListModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    queryset = Signature.objects.all()
    serializer_class = SignatureSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(order=self.kwargs['orders_pk'])
        return queryset

    def get_serializer_context(self):
        """
        Query accounts, projects and employee information for to_represtation() function
        """
        # TODO Use asyncio to speed up the reuqest with third-party api
        context = super().get_serializer_context()

        # Get project information
        project_object = cache.get('projects', None)
        if project_object is None:
            project_object = {}
            status, results = self.get_project_via_search()

            if status and results:
                serializer = ProjectEasySerializer(results, many=True)
                for project in serializer.data:
                    project_id = project['id']
                    if project_id not in project_object:
                        project_object[project_id] = project
                cache.set('projects', project_object, 60 * 60)
        context['projects'] = project_object

        # Get account information
        account_object = cache.get('accounts', None)
        if account_object is None:
            account_object = {}
            status, results = self.get_account_via_search()

            if status and results:
                serializer = AccountEasySerializer(results, many=True)
                for account in serializer.data:
                    account_id = account['id']
                    if account_id not in account_object:
                        account_object[account_id] = account
                cache.set('accounts', account_object, 60 * 60)
        context['accounts'] = account_object

        # Get employee information
        employee_object = cache.get('employees', None)
        if employee_object is None:
            instance = Employee.objects.using('hr').all().values()
            serializer = EmployeeNonModelSerializer(instance, many=True)

            employee_object = {}
            for employee in serializer.data:
                employee_id = employee['employee_id']
                if employee_id not in employee_object:
                    employee_object[employee_id] = employee
            cache.set('employees', employee_object, 60 * 60)
        context['employees'] = employee_object

        return context

    def perform_update(self, serializer):
        serializer.save(signed_time=timezone.now())
        signature_id = serializer.data['id']
        signature = Signature.objects.get(pk=signature_id)
        direction_flag = signature.status
        order = Order.objects.get(pk=signature.order.id)

        # Save to OrderTracker
        order_tracker_serializer = OrderTrackerSerializer(data=model_to_dict(order))
        if order_tracker_serializer.is_valid(raise_exception=True):
            order_tracker_serializer.save(
                order=order,
                form_begin_time=order.form_begin_time,
                form_end_time=order.form_end_time,
                update_time=order.update_time
            )

        link = f"{self.request.build_absolute_uri(location='/')}?order={order.id}"
        if direction_flag == 'Approve':
            if 'P1' in order.status:
                skip_signature_flag, create_new_signaure_flag = self.calculate_signature_flag(order.id, 'P1')
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
                elif not skip_signature_flag:
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
                skip_signature_flag, create_new_signaure_flag = self.calculate_signature_flag(order.id, 'P4')
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
                elif not skip_signature_flag:
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
                        'signed_time': '',
                        'role_group': signature.role_group,
                        'order': order
                    }
                    Signature.objects.create(**next_signature)
                    # Send email to next signer
                    self.send_mail_2_single_user(next_signer, link, category='signing')

            # Send notification to all order attendent
            category = 'signature'
            actor = self.request.user.get_english_name()
            verb = 'approve'
            action_object = 'order'
            self.send_notification(order.id, link, category, actor, verb, action_object)

        elif direction_flag == 'Return':
            if 'P1' in order.status:
                skip_signature_flag, create_new_signaure_flag = self.calculate_signature_flag(order.id, 'P1')
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
                skip_signature_flag, create_new_signaure_flag = self.calculate_signature_flag(order.id, 'P4')
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

            # Send notification to all order attendent
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
            elif 'P4' in order.status:
                # Order staus change
                order.status = {
                    'P4': {
                        signature.signer: 'Close'
                    }
                }
                order.form_end_time = timezone.now()
                order.save()
                # Send close order mail to all member
                self.send_mail_2_all(order.id, link, category='close')

            # Send notification to all order attendent
            category = 'signature'
            actor = self.request.user.get_english_name()
            verb = 'close'
            action_object = 'order'
            self.send_notification(order.id, link, category, actor, verb, action_object)
