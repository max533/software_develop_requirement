""" singature app's api viewsets.py """
import json
import logging

from develop_requirement_proj.employee.api.serializers import (
    EmployeeSerializer,
)
from develop_requirement_proj.employee.models import Employee
from develop_requirement_proj.utils.mixins import QueryDataMixin

from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db.models import Max
from django.forms import model_to_dict
from django.utils import timezone

from rest_framework import mixins, response, serializers, views, viewsets
from rest_framework.decorators import action

from ..models import (
    Account, Document, History, Notification, Order, OrderTracker, Progress,
    Project, Schedule, ScheduleTracker, Signature,
)
from .filters import OrderFilter, OrderFilterBackend
from .paginations import OrderPagination
from .serializers import (
    AccountEasySerializer, AccountSerializer, DocumentSerializer,
    EmployeeNonModelSerializer, HistorySerializer, NotificationSerializer,
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


class ScheduleViewSet(viewsets.ModelViewSet):
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
        try:
            signature = order.signature_set.filter(role_group='assigner').latest('signed_time')
            signer = signature.signer
            signer_department_id = Employee.objects.using('hr').get(employee_id__iexact=signer).department_id
            count = 0
            for char in signer_department_id[::-1]:
                if char == '0':
                    count += 1
                elif char != '0':
                    break
            if count >= 4:
                skip_signature_flag = True
            elif count < 4:
                skip_signature_flag = False
        except ObjectDoesNotExist as err:
            logger.info(f"There are not any signature. Error Message: {err}")
            skip_signature_flag = False
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
        try:
            signature = order.signature_set.filter(role_group='assigner').latest('signed_time')
            signer = signature.signer
            signer_department_id = Employee.objects.using('hr').get(employee_id__iexact=signer).department_id
            count = 0
            for char in signer_department_id[::-1]:
                if char == '0':
                    count += 1
                elif char != '0':
                    break
            if count >= 4:
                skip_signature_flag = True
            elif count < 4:
                skip_signature_flag = False
        except ObjectDoesNotExist as err:
            logger.info(f"There are not any signature. Error Message: {err}")
            skip_signature_flag = False

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
        try:
            signature = order.signature_set.filter(role_group='assigner').latest('signed_time')
            signer = signature.signer
            signer_department_id = Employee.objects.using('hr').get(employee_id__iexact=signer).department_id
            count = 0
            for char in signer_department_id[::-1]:
                if char == '0':
                    count += 1
                elif char != '0':
                    break
            if count >= 4:
                skip_signature_flag = True
            elif count < 4:
                skip_signature_flag = False
        except ObjectDoesNotExist as err:
            logger.info(f"There are not any signature in P4. Error Message: {err}")
            skip_signature_flag = False

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


class HistoryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ Provide History resource with `list` and `create` action """
    queryset = History.objects.all()
    serializer_class = HistorySerializer

    def get_queryset(self):
        """ Filter History by order_id """
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


class NotificationVewSet(mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        """ Get current user's notification """
        queryset = []
        employee_id = self.request.user.username
        queryset = self.queryset.filter(owner=employee_id)
        return queryset


class OrderViewSet(QueryDataMixin,
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

        if self.action in ['create', 'update']:
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
        serializer.save(initiator=self.request.user.username)

        order_id = serializer.instance.id
        order = Order.objects.get(pk=order_id)
        order_status = order.status

        # Save OrderTracker
        order_tracker_serializer = OrderTrackerSerializer(data=model_to_dict(order))
        if order_tracker_serializer.is_valid(raise_exception=True):
            order_tracker_serializer.save(order=order, form_begin_time=order.form_begin_time)

        # # Create History (including last record and update content with json)'
        comment = {
            'last_order': '',
            'current_order': serializer.data
        }
        history = {
            'editor': 'system',
            'comment': json.dumps(comment),
            'order': order
        }
        History.objects.create(**history)

        if 'P0' in order_status:
            direction_flag = order_status['P0'].get('initiator', None)
            if direction_flag == 'Approve':
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}'"
                )
                logger.debug(debug_message)
                # Find next signer
                signer = order.initiator
                signer_department_id = Employee.objects.using('hr').get(employee_id__iexact=signer).department_id
                status, result = self.get_department_via_query(department_id=signer_department_id)
                if not (status and result):
                    warn_message = (
                        f"It couldn't be find next signer with the current signer '{signer}'"
                    )
                    logger.warning(warn_message)
                    return
                if signer_department_id in result:
                    next_signer = result[signer_department_id].get('dm', None)
                # If initiator is equal to next_signer
                if signer == next_signer:
                    count = 0
                    for char in signer_department_id[::-1]:
                        if char == '0':
                            count += 1
                        elif char != '0':
                            break
                    non_zero_part = len(signer_department_id) - count - 1
                    next_signer_department_id = signer_department_id[:non_zero_part] + '0' * (count + 1)
                    status, result = self.get_department_via_query(department_id=next_signer_department_id)
                    if not (status and result):
                        warn_message = (
                            f"It couldn't be find next signer with the current signer '{signer}'"
                        )
                        logger.warning(warn_message)
                        return
                    if next_signer_department_id in result:
                        next_signer = result[next_signer_department_id].get('dm', None)
                else:
                    next_signer_department_id = signer_department_id
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
                # Order Status Change
                order.status = {
                    "P1": {
                        next_signer: ""
                    }
                }
                order.save()
                # Send Email to next signer
                email_subject = "<Signing> There is a software development order waiting your signing"
                recipient_name = Employee.objects.using('hr').get(employee_id=next_signer).english_name.title()
                email_message = (
                    f"Dear {recipient_name},\n" +
                    "\n" +
                    "There is a software developement order that is waiting for your signing.\n" +
                    "You can click below link to check the order detail.\n" +
                    f"{self.request.build_absolute_uri(location='/')}?order={order_id} \n"
                    "\n" +
                    "Don't reply this mail as it is automatically sent by the system.\n" +
                    "If you have any question, welcome to contact DQMS Team.\n" +
                    "\n" +
                    "Best Regard\n" +
                    "DQMS Software Developement Requirement System Administrator <dqms_admin@wistron.com>"
                )
                sender = ""
                recipient_list = [Employee.objects.using('hr').get(employee_id=next_signer).mail]
                send_mail(email_subject, email_message, sender, recipient_list)
            elif direction_flag == 'Close':
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}'"
                )
                logger.debug(debug_message)
                order.form_end_time = timezone.now()
                order.save()
        # Send Notification to all member

    def perform_update(self, serializer):
        serializer.save()
        # P1 and P4 status change in signature api
        order_id = serializer.data['id']
        order = Order.objects.get(pk=order_id)
        order_status = order.status

        # Create History (including last record and update content with json)
        last_order_tracker = dict(OrderTracker.objects.filter(order=order_id).order_by('created_time').values()[0])
        del last_order_tracker['order_id']
        kwargs = {}
        kwargs['context'] = {'accounts': cache.get('accounts', None)}
        kwargs['context'].update({'projects': cache.get('projects', None)})
        kwargs['context'].update({'employees': cache.get('employees', None)})

        comment = {
            'last_order': OrderDynamicSerializer(last_order_tracker, **kwargs).data,
            'update_content': serializer.data
        }
        history = {
            'editor': 'system',
            'comment': json.dumps(comment),
            'order': order
        }
        History.objects.create(**history)

        # Save OrderTracker
        order_tracker_serializer = OrderTrackerSerializer(data=model_to_dict(order))
        if order_tracker_serializer.is_valid(raise_exception=True):
            order_tracker_serializer.save(order=order, form_begin_time=order.form_begin_time)

        if 'P0' in order_status:
            direction_flag = order_status['P0'].get('initiator', None)

            if direction_flag is None or direction_flag == "":
                error_message = (
                    f"The status of order id '{order_id}'  is not correct." +
                    "There are not correct direction_flag attribure in order status."
                )
                logger.error(error_message)
            elif direction_flag == "Approve":
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}'"
                )
                logger.debug(debug_message)
                # Check signature stage is finished or not. The last signer will function head leader.
                # Consecutive occurrences times of the zero in department_id is greater than four.
                signer = order.signature_set.filter(role_group='initiator').latest('signed_time').signer
                signer_department_id = Employee.objects.using('hr').get(employee_id__iexact=signer).department_id
                count = 0
                for char in signer_department_id[::-1]:
                    if char == '0':
                        count += 1
                    elif char != '0':
                        break
                if count >= 4:
                    skip_signature_flag = True
                elif count < 4:
                    skip_signature_flag = False

                if skip_signature_flag:
                    # Debug Code
                    debug_message = (
                        f"Order Status:'{order_status}', direction_flag:'{direction_flag}', " +
                        f"skip_signature_flag:'{skip_signature_flag}'"
                    )
                    logger.debug(debug_message)
                    order.status = {
                        "P2": {
                            "assigner": ""
                        }
                    }
                    order.save()
                    # TODO Send email to assigner
                    email_subject = "<Confirm> There is a software development order waiting your confirm."
                    recipient_name = Employee.objects.using('hr').get(employee_id=order.assigner).english_name.title()
                    email_message = (
                        f"Dear {recipient_name},\n" +
                        "\n" +
                        "There is a software developement order that is waiting for your response.\n" +
                        "You can click below link to check the order detail.\n" +
                        f"{self.request.build_absolute_uri(location='/')}?order={order_id} \n"
                        "\n" +
                        "Don't reply this mail as it is automatically sent by the system.\n" +
                        "If you have any question, welcome to contact DQMS Team.\n" +
                        "\n" +
                        "Best Regard\n" +
                        "DQMS Software Developement Requirement System Administrator <dqms_admin@wistron.com>"
                    )
                    sender = ""
                    recipient_list = [Employee.objects.using('hr').get(employee_id=order.assigner).mail]
                    send_mail(email_subject, email_message, sender, recipient_list)
                elif not skip_signature_flag:
                    # Debug Code
                    debug_message = (
                        f"Order Status:'{order_status}', direction_flag:'{direction_flag}'," +
                        f"skip_signature_flag:'{skip_signature_flag}'"
                    )
                    logger.debug(debug_message)
                    # Find next Singer
                    signer = order.initiator
                    signer_department_id = Employee.objects.using('hr').get(employee_id__iexact=signer).department_id
                    status, result = self.get_department_via_query(department_id=signer_department_id)
                    if not (status and result):
                        warn_message = (
                            f"It couldn't be find next signer with the current signer '{signer}'"
                        )
                        logger.warning(warn_message)
                        return

                    if signer_department_id in result:
                        next_signer = result[signer_department_id].get('dm', None)
                    # If initiator is equal to next_signer
                    if signer == next_signer:
                        non_zero_part = len(signer_department_id) - count - 1
                        next_signer_department_id = signer_department_id[:non_zero_part] + '0' * (count + 1)
                        status, result = self.get_department_via_query(department_id=next_signer_department_id)
                        if not (status and result):
                            warn_message = (
                                f"It couldn't be find next signer with the current signer '{signer}'"
                            )
                            logger.warning(warn_message)
                            return
                        if next_signer_department_id in result:
                            next_signer = result[next_signer_department_id].get('dm', None)
                    else:
                        next_signer_department_id = signer_department_id
                    # Check whether enter next phase or not
                    max_sequence = order.signature_set.aggregate(Max('sequence'))['sequence__max']
                    if order.signature_set.get(sequence=max_sequence).status in ['Approve', 'Return']:
                        # Create next Signature
                        sequence_max = order.signature_set.aggregate(Max('sequence'))['sequence__max']
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
                        # TODO Send email to next signer
                        email_subject = "<Signing> There is a software development order waiting your signing"
                        recipient_name = Employee.objects.using('hr').get(employee_id=next_signer).english_name.title()
                        email_message = (
                            f"Dear {recipient_name},\n" +
                            "\n" +
                            "There is a software developement order that is waiting for your signing.\n" +
                            "You can click below link to check the order detail.\n" +
                            f"{self.request.build_absolute_uri(location='/')}?order={order_id} \n"
                            "\n" +

                            "Don't reply this mail as it is automatically sent by the system.\n" +
                            "If you have any question, welcome to contact DQMS Team.\n" +
                            "\n" +
                            "Best Regard\n" +
                            "DQMS Software Developement Requirement System Administrator <dqms_admin@wistron.com>"
                        )
                        sender = ""
                        recipient_list = [Employee.objects.using('hr').get(employee_id=next_signer).mail]
                        send_mail(email_subject, email_message, sender, recipient_list)
            elif direction_flag == "Close":
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}'"
                )
                logger.debug(debug_message)
                order.form_end_time = timezone.now()
                order.save()
                # TODO Send email to all member
                email_subject = "<Close> There is a software development closed order"
                email_message = (
                    "Dear all,\n" +
                    "\n" +
                    "There is a software developement closed order.\n" +
                    "You can click below link to check the order detail.\n" +
                    f"{self.request.build_absolute_uri(location='/')}?order={order_id} \n" +
                    "\n" +
                    "Don't reply this mail as it is automatically sent by the system.\n" +
                    "If you have any question, welcome to contact DQMS Team.\n" +
                    "\n" +
                    "Best Regard\n" +
                    "DQMS Software Developement Requirement System Administrator <dqms_admin@wistron.com>"
                )
                sender = ""
                # Collect all member mail in recipient_list
                signer_id_list = list(order.signature_set.order_by(
                    'signer').distinct('signer').values_list('signer', flat=True))
                signer_mail_list = list(Employee.objects.using('hr').filter(
                    employee_id__in=signer_id_list).values_list('mail', flat=True))

                developers = order.developers
                developer_list = []
                if 'contactor' in developers:
                    developer_list.append(developers['contactor'])
                if 'member' in developers:
                    developer_list.extend(developers['member'])
                developer_mail_list = list(Employee.objects.using('hr').filter(
                    employee_id__in=developer_list).values_list('mail', flat=True))

                recipient_list = [
                    Employee.objects.using('hr').get(employee_id=order.assigner).mail,
                    Employee.objects.using('hr').get(employee_id=order.initiator).mail,
                ]
                recipient_list.extend(
                    [mail for mail in signer_mail_list if mail not in recipient_list]
                )
                recipient_list.extend(
                    [mail for mail in developer_mail_list if mail not in recipient_list]
                )
                send_mail(email_subject, email_message, sender, recipient_list)
        elif 'P2' in order_status:
            direction_flag = order_status['P2'].get('assigner', None)

            if direction_flag is None or direction_flag == "":
                error_message = (
                    f"The status of order id '{order_id}' is not correct. " +
                    "There are not correct direction_flag attribure in order status."
                )
                logger.error(error_message)
            elif direction_flag == "Approve":
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}'"
                )
                logger.debug(debug_message)
                order.status = {
                    "P3": {
                        "initiator": "",
                        "assigner": "",
                        "developers": ""
                    },
                    "signed": False
                }
                order.save()
                # TODO Send email to assigner
                email_subject = "Schedule: There is a software development order waiting your schedule"
                recipient_name = Employee.objects.using('hr').get(employee_id=order.assigner).english_name.title()
                email_message = (
                    f"Dear {recipient_name},\n" +
                    "\n" +
                    "There is a software developement order that is waiting for your schedule.\n" +
                    "You can click below link to check the order detail.\n" +
                    f"{self.request.build_absolute_uri(location='/')}?order={order_id} \n"
                    "\n" +

                    "Don't reply this mail as it is automatically sent by the system.\n" +
                    "If you have any question, welcome to contact DQMS Team.\n" +
                    "\n" +
                    "Best Regard\n" +
                    "DQMS Software Developement Requirement System Administrator <dqms_admin@wistron.com>"
                )
                sender = ""
                recipient_list = [Employee.objects.using('hr').get(employee_id=order.assigner).mail.lower()]
                send_mail(email_subject, email_message, sender, recipient_list)
            elif direction_flag == "Return":
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}'"
                )
                logger.debug(debug_message)
                # Check signature stage is finished or not. The last signer will function head leader.
                # Consecutive occurrences times of the zero in department_id is greater than four.
                try:
                    signer = order.signature_set.filter(
                        role_group='initiator', signed_time__isnull=False).latest('signed_time').signer
                except ObjectDoesNotExist as err:
                    warn_message = (
                        f"It can't find any signature with order id {order.id}. Warn Message: {err}"
                    )
                    logger.warn(warn_message)
                    return
                signer_department_id = Employee.objects.using('hr').get(employee_id__iexact=signer).department_id
                count = 0
                for char in signer_department_id[::-1]:
                    if char == '0':
                        count += 1
                    elif char != '0':
                        break
                if count >= 4:
                    skip_signature_flag = True
                    # Debug Code
                    debug_message = (
                        f"Order Status:'{order_status}', direction_flag:'{direction_flag}', " +
                        f"skip_signature_flag:'{skip_signature_flag}'"
                    )
                    logger.debug(debug_message)
                    order.status = {
                        'P0': {
                            'initiator': ''
                        },
                        'signed': skip_signature_flag
                    }
                    order.save()
                elif count < 4:
                    skip_signature_flag = False
                    # Debug Code
                    debug_message = (
                        f"Order Status:'{order_status}', direction_flag:'{direction_flag}', " +
                        f"skip_signature_flag:'{skip_signature_flag}'"
                    )
                    logger.debug(debug_message)
                    order.status = {
                        'P0': {
                            'initiator': ''
                        },
                        'signed': skip_signature_flag
                    }
                    order.save()
                # TODO Send email to initiator
                email_subject = "<Return> There is a software development return order waiting your confirm"
                recipient_name = Employee.objects.using('hr').get(employee_id=order.initiator).english_name.title()
                email_message = (
                    f"Dear {recipient_name},\n" +
                    "\n" +
                    "There is a software developement return order that is waiting for your response.\n" +
                    "You can click below link to check the order detail.\n" +
                    f"{self.request.build_absolute_uri(location='/')}?order={order_id} \n"
                    "\n" +

                    "Don't reply this mail as it is automatically sent by the system.\n" +
                    "If you have any question, welcome to contact DQMS Team.\n" +
                    "\n" +
                    "Best Regard\n" +
                    "DQMS Software Developement Requirement System Administrator <dqms_admin@wistron.com>"
                )
                sender = ""
                recipient_list = [Employee.objects.using('hr').get(employee_id=order.initiator).mail]
                send_mail(email_subject, email_message, sender, recipient_list)
            elif direction_flag == "Close":
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}'"
                )
                logger.debug(debug_message)
                order.form_end_time = timezone.now()
                order.save()
                # Send email to all member
                email_subject = "<Close> There is a software development closed order"
                email_message = (
                    "Dear all,\n" +
                    "\n" +
                    "There is a software developement closed order.\n" +
                    "You can click below link to check the order detail.\n" +
                    f"{self.request.build_absolute_uri(location='/')}?order={order.id} \n" +
                    "\n" +
                    "Don't reply this mail as it is automatically sent by the system.\n" +
                    "If you have any question, welcome to contact DQMS Team.\n" +
                    "\n" +
                    "Best Regard\n" +
                    "DQMS Software Developement Requirement System Administrator <dqms_admin@wistron.com>"
                )
                sender = ""
                # Collect all member mail in recipient_list
                signer_id_list = list(order.signature_set.order_by(
                    'signer').distinct('signer').values_list('signer', flat=True))
                signer_mail_list = list(Employee.objects.using('hr').filter(
                    employee_id__in=signer_id_list).values_list('mail', flat=True))

                developers = order.developers
                developer_list = []
                if 'contactor' in developers:
                    developer_list.append(developers['contactor'])
                if 'member' in developers:
                    developer_list.extend(developers['member'])

                developer_mail_list = list(Employee.objects.using('hr').filter(
                    employee_id__in=developer_list).values_list('mail', flat=True))

                recipient_list = [
                    Employee.objects.using('hr').get(employee_id=order.assigner).mail,
                    Employee.objects.using('hr').get(employee_id=order.initiator).mail,
                ]
                recipient_list.extend(
                    [mail for mail in signer_mail_list if mail not in recipient_list]
                )
                recipient_list.extend(
                    [mail for mail in developer_mail_list if mail not in recipient_list]
                )
                send_mail(email_subject, email_message, sender, recipient_list)
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
            elif status_list[1] == "Approve":
                direction_flag = "Negotiate"
            else:
                direction_flag = "Wait"

            if direction_flag in ['Return', 'Approve', 'Wait', 'Negotiate', "Close"]:
                # Check signature stage is finished or not. The last signer will function head leader.
                # Consecutive occurrences times of the zero in department_id is greater than four.
                try:
                    signature = order.signature_set.filter(role_group='assigner').latest('signed_time')
                    signer = signature.signer
                    signer_department_id = Employee.objects.using('hr').get(employee_id__iexact=signer).department_id
                    count = 0
                    for char in signer_department_id[::-1]:
                        if char == '0':
                            count += 1
                        elif char != '0':
                            break
                    if count >= 4:
                        skip_signature_flag = True
                    elif count < 4:
                        skip_signature_flag = False
                except ObjectDoesNotExist as err:
                    logger.info(f"There are not any signature. Error Message: {err}")
                    skip_signature_flag = False

            if direction_flag == "Approve":
                # Check the all schedule modify or not.
                # If schedule didn't be modified, It will skip bleow thing.
                # 1. Recalculate the schedule version and record snapshot in ScheduleTracker table
                # 2. Change schedule's expected_time to actual_time
                # 3. Change schedule's all confirm status to True
                objs = order.schedule_set.all()
                if not all(list(objs.values_list('confirm_status', flat=True))):
                    current_max_version = objs.aggregate(Max('version'))['version__max']
                    new_version = 1 if current_max_version is None else current_max_version + 1
                    for obj in objs:
                        obj.actual_time, obj.expected_time = obj.expected_time, None
                        obj.version = new_version
                        obj.confirm_status = True
                    Schedule.objects.bulk_update(objs, ['actual_time', 'expected_time', 'version', 'confirm_status'])
                    result = ScheduleTracker.objects.aggregate(Max('id'))['id__max']
                    new_id = 0 if result is None else result
                    for obj in objs:
                        new_id += 1
                        obj.id = new_id
                    ScheduleTracker.objects.bulk_create(objs)

                if skip_signature_flag:
                    # Debug Code
                    debug_message = (
                        f"Order Status:'{order_status}', direction_flag:'{direction_flag}', " +
                        f"skip_signature_flag:'{skip_signature_flag}'"
                    )
                    logger.debug(debug_message)
                    order.status = {
                        "P5": {
                            "developers": ""
                        }
                    }
                    order.save()
                    # TODO Send email to developers
                    email_subject = "<Confirm> There is a software development order waiting your confirm."
                    recipient_name = Employee.objects.using('hr').get(
                        employee_id=order.developers['contactor']).english_name.title()
                    email_message = (
                        f"Dear {recipient_name} & developers,\n" +
                        "\n" +
                        "There is a software developement order that is waiting for your response.\n" +
                        "You can click below link to check the order detail.\n" +
                        f"{self.request.build_absolute_uri(location='/')}?order={order.id} \n"
                        "\n" +
                        "Don't reply this mail as it is automatically sent by the system.\n" +
                        "If you have any question, welcome to contact DQMS Team.\n" +
                        "\n" +
                        "Best Regard\n" +
                        "DQMS Software Developement Requirement System Administrator <dqms_admin@wistron.com>"
                    )
                    sender = ""
                    developers = order.developers
                    developer_list = []
                    if 'contactor' in developers:
                        developer_list.append(developers['contactor'])
                    if 'member' in developers:
                        developer_list.append(developers['member'])
                    developer_mail_list = set(Employee.objects.using('hr').filter(
                        employee_id__in=developer_list).values_list('mail', flat=True))
                    recipient_list = developer_list
                    send_mail(email_subject, email_message, sender, recipient_list)
                elif not skip_signature_flag:
                    # Debug Code
                    debug_message = (
                        f"Order Status:'{order_status}', direction_flag:'{direction_flag}', " +
                        f"skip_signature_flag:'{skip_signature_flag}'"
                    )
                    logger.debug(debug_message)

                    # Find next Singer
                    signer = order.assigner
                    signer_department_id = Employee.objects.using('hr').get(employee_id__iexact=signer).department_id
                    status, result = self.get_department_via_query(department_id=signer_department_id)
                    if not (status and result):
                        warn_message = (
                            f"It couldn't be find next signer with the current signer '{signer}'"
                        )
                        logger.warning(warn_message)
                        return
                    if signer_department_id in result:
                        next_signer = result[signer_department_id].get('dm', None)
                    # If assigner is equal to next_signer
                    count = 0
                    for char in signer_department_id[::-1]:
                        if char == '0':
                            count += 1
                        elif char != '0':
                            break
                    if signer == next_signer:
                        non_zero_part = len(signer_department_id) - count - 1
                        next_signer_department_id = signer_department_id[:non_zero_part] + '0' * (count + 1)
                        status, result = self.get_department_via_query(department_id=next_signer_department_id)
                        if not (status and result):
                            warn_message = (
                                f"It couldn't be find next signer with the current signer '{signer}'"
                            )
                            logger.warning(warn_message)
                            return
                        if next_signer_department_id in result:
                            next_signer = result[next_signer_department_id].get('dm', None)
                    else:
                        next_signer_department_id = signer_department_id
                    # Check whether enter next phase or not
                    max_sequence = order.signature_set.aggregate(Max('sequence'))['sequence__max']
                    if order.signature_set.get(sequence=max_sequence).status in ['Approve', 'Return']:
                        # Create Signature
                        sequence_max = order.signature_set.aggregate(Max('sequence'))['sequence__max']
                        next_signature = {
                            'sequence': sequence_max + 1,
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
                        # TODO Send email to next signer
                        email_subject = "<Signing> There is a software development order waiting your signing"
                        recipient_name = Employee.objects.using('hr').get(employee_id=next_signer).english_name.title()
                        email_message = (
                            f"Dear {recipient_name},\n" +
                            "\n" +
                            "There is a software developement order that is waiting for your signing.\n" +
                            "You can click below link to check the order detail.\n" +
                            f"{self.request.build_absolute_uri(location='/')}?order={order_id} \n"
                            "\n" +
                            "Don't reply this mail as it is automatically sent by the system.\n" +
                            "If you have any question, welcome to contact DQMS Team.\n" +
                            "\n" +
                            "Best Regard\n" +
                            "DQMS Software Developement Requirement System Administrator <dqms_admin@wistron.com>"
                        )
                        sender = ""
                        recipient_list = [Employee.objects.using('hr').get(employee_id=next_signer).mail]
                        send_mail(email_subject, email_message, sender, recipient_list)
            elif direction_flag == "Return":
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}'"
                )
                logger.debug(debug_message)

                order.status = {
                    "P3": {
                        "initiator": "",
                        "assigner": "",
                        "developers": ""
                    },
                    "signed": skip_signature_flag
                }
                order.save()
                # TODO Send email to assigner
                email_subject = "ReSchedule: There is a software development order waiting your reschedule"
                recipient_name = Employee.objects.using('hr').get(employee_id=order.assigner).english_name.title()
                email_message = (
                    f"Dear {recipient_name},\n" +
                    "\n" +
                    "There is a software developement return order that is waiting for your reschedule.\n" +
                    "You can click below link to check the order detail.\n" +
                    f"{self.request.build_absolute_uri(location='/')}?order={order_id} \n"
                    "\n" +
                    "Don't reply this mail as it is automatically sent by the system.\n" +
                    "If you have any question, welcome to contact DQMS Team.\n" +
                    "\n" +
                    "Best Regard\n" +
                    "DQMS Software Developement Requirement System Administrator <dqms_admin@wistron.com>"
                )
                sender = ""
                recipient_list = [Employee.objects.using('hr').get(employee_id=order.assigner).mail]
                send_mail(email_subject, email_message, sender, recipient_list)
            elif direction_flag == "Close":
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}'"
                )
                logger.debug(debug_message)
                order.status = {
                    "P3": {
                        "assigner": "Close",
                    },
                    "signed": skip_signature_flag
                }
                order.form_end_time = timezone.now()
                order.save()
                # TODO Send email to all member
                email_subject = "<Close> There is a software development closed order"
                email_message = (
                    "Dear all,\n" +
                    "\n" +
                    "There is a software developement closed order.\n" +
                    "You can click below link to check the order detail.\n" +
                    f"{self.request.build_absolute_uri(location='/')}?order={order.id} \n" +
                    "\n" +
                    "Don't reply this mail as it is automatically sent by the system.\n" +
                    "If you have any question, welcome to contact DQMS Team.\n" +
                    "\n" +
                    "Best Regard\n" +
                    "DQMS Software Developement Requirement System Administrator <dqms_admin@wistron.com>"
                )
                sender = ""
                # Collect all member mail in recipient_list
                signer_id_list = list(order.signature_set.order_by(
                    'signer').distinct('signer').values_list('signer', flat=True))
                signer_mail_list = list(Employee.objects.using('hr').filter(
                    employee_id__in=signer_id_list).values_list('mail', flat=True))

                developers = order.developers
                developer_list = []
                if 'contactor' in developers:
                    developer_list.append(developers['contactor'])
                if 'member' in developers:
                    developer_list.extend(developers['member'])

                developer_mail_list = list(Employee.objects.using('hr').filter(
                    employee_id__in=developer_list).values_list('mail', flat=True))

                recipient_list = [
                    Employee.objects.using('hr').get(employee_id=order.assigner).mail,
                    Employee.objects.using('hr').get(employee_id=order.initiator).mail,
                ]
                recipient_list.extend(
                    [mail for mail in signer_mail_list if mail not in recipient_list]
                )
                recipient_list.extend(
                    [mail for mail in developer_mail_list if mail not in recipient_list]
                )
                send_mail(email_subject, email_message, sender, recipient_list)

            elif direction_flag == "Wait":
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}'"
                )
                logger.debug(debug_message)
                order.status['signed'] = skip_signature_flag
                order.save()

            elif direction_flag == "Negotiate":
                # Debug Code
                debug_message = (
                    f"Order Status:'{order_status}', direction_flag:'{direction_flag}'"
                )
                logger.debug(debug_message)
                order.status['signed'] = skip_signature_flag
                # Send email to initiator and developers contactor
                email_subject = "<Confirm> There is a software development order waiting your confirm"
                if 'contactor' in order.developers:
                    developer_contactor = order.developers['contactor']
                recipient_name_list = [
                    Employee.objects.using('hr').get(employee_id=order.initiator).english_name.title(),
                    Employee.objects.using('hr').get(employee_id=developer_contactor).english_name.title()
                ]
                recipient_name = ' & '.join(recipient_name_list)
                email_message = (
                    f"Dear {recipient_name},\n" +
                    "\n" +
                    "There is a software developement order that is waiting for your response.\n" +
                    "You can click below link to check the order detail.\n" +
                    f"{self.request.build_absolute_uri(location='/')}?order={order_id} \n"
                    "\n" +
                    "Don't reply this mail as it is automatically sent by the system.\n" +
                    "If you have any question, welcome to contact DQMS Team.\n" +
                    "\n" +
                    "Best Regard\n" +
                    "DQMS Software Developement Requirement System Administrator <dqms_admin@wistron.com>"
                )
                sender = ""
                recipient_list = [
                    Employee.objects.using('hr').get(employee_id=order.initiator).mail,
                    Employee.objects.using('hr').get(employee_id=developer_contactor).mail,
                ]
                send_mail(email_subject, email_message, sender, recipient_list)

        elif 'P5' in order_status:

            if 'developers' in order_status['P5']:
                direction_flag = order_status['P5'].get('developers', None)
                if direction_flag is None or direction_flag == "":
                    error_message = (
                        f"The status of order id '{order_id}'  is not correct." +
                        "There are not correct direction_flag attribure in order status."
                    )
                    logger.error(error_message)
                elif direction_flag == "Approve":
                    # Debug Code
                    debug_message = (
                        f"Order Status:'{order_status}', direction_flag:'{direction_flag}'"
                    )
                    logger.debug(debug_message)
                    order.status = {
                        "P5": {
                            "initiator": ""
                        }
                    }
                    order.save()
                # TODO Send email to initiator
                email_subject = "<Confirm> There is a software development order waiting your confirm"
                recipient_name = Employee.objects.using('hr').get(employee_id=order.initiator).english_name.title()
                email_message = (
                    f"Dear {recipient_name},\n" +
                    "\n" +
                    "There is a software developement order waiting for your response.\n" +
                    "You can click below link to check the order detail.\n" +
                    f"{self.request.build_absolute_uri(location='/')}?order={order_id} \n"
                    "\n" +
                    "Don't reply this mail as it is automatically sent by the system.\n" +
                    "If you have any question, welcome to contact DQMS Team.\n" +
                    "\n" +
                    "Best Regard\n" +
                    "DQMS Software Developement Requirement System Administrator <dqms_admin@wistron.com>"
                )
                sender = ""
                recipient_list = [Employee.objects.using('hr').get(employee_id=order.initiator).mail]
                send_mail(email_subject, email_message, sender, recipient_list)

            elif 'initiator' in order_status['P5']:
                direction_flag = order_status['P5'].get('initiator', None)
                if direction_flag is None or direction_flag == "":
                    error_message = (
                        f"The status of order id '{order_id}'  is not correct." +
                        "There are not correct direction_flag attribure in order status."
                    )
                    logger.error(error_message)
                elif direction_flag == "Approve":
                    # Debug Code
                    debug_message = (
                        f"Order Status:'{order_status}', direction_flag:'{direction_flag}'"
                    )
                    logger.debug(debug_message)
                    # TODO Send email to all member
                    email_subject = "<Complete> There is a software development complete order"
                    email_message = (
                        "Dear all,\n" +
                        "\n" +
                        "There is a software developement complete order.\n" +
                        "You can click below link to check the order detail.\n" +
                        f"{self.request.build_absolute_uri(location='/')}?order={order.id} \n" +
                        "\n" +
                        "Don't reply this mail as it is automatically sent by the system.\n" +
                        "If you have any question, welcome to contact DQMS Team.\n" +
                        "\n" +
                        "Best Regard\n" +
                        "DQMS Software Developement Requirement System Administrator <dqms_admin@wistron.com>"
                    )
                    sender = ""
                    # Collect all member mail in recipient_list
                    signer_id_list = list(order.signature_set.order_by(
                        'signer').distinct('signer').values_list('signer', flat=True))
                    signer_mail_list = list(Employee.objects.using('hr').filter(
                        employee_id__in=signer_id_list).values_list('mail', flat=True))

                    developers = order.developers
                    developer_list = []
                    if 'contactor' in developers:
                        developer_list.append(developers['contactor'])
                    if 'member' in developers:
                        developer_list.extend(developers['member'])
                    developer_mail_list = list(Employee.objects.using('hr').filter(
                        employee_id__in=developer_list).values_list('mail', flat=True))

                    recipient_list = [
                        Employee.objects.using('hr').get(employee_id=order.assigner).mail,
                        Employee.objects.using('hr').get(employee_id=order.initiator).mail,
                    ]
                    recipient_list.extend(
                        [mail for mail in signer_mail_list if mail not in recipient_list]
                    )
                    recipient_list.extend(
                        [mail for mail in developer_mail_list if mail not in recipient_list]
                    )
                    send_mail(email_subject, email_message, sender, recipient_list)
                elif direction_flag == "Return":
                    # Debug Code
                    debug_message = (
                        f"Order Status:'{order_status}', direction_flag:'{direction_flag}'"
                    )
                    logger.debug(debug_message)
                    order.status = {
                        "P5": {
                            "developers": ""
                        }
                    }
                    order.save()
                    # TODO Send email to developers
                    email_subject = "<Return> There is a software development return order waiting your confirm."
                    recipient_name = Employee.objects.using('hr').get(
                        employee_id=order.developers['contactor']).english_name.title()
                    email_message = (
                        f"Dear {recipient_name} & developers,\n" +
                        "\n" +
                        "There is a software developement return order that is waiting for your response.\n" +
                        "You can click below link to check the order detail.\n" +
                        f"{self.request.build_absolute_uri(location='/')}?order={order.id} \n"
                        "\n" +
                        "Don't reply this mail as it is automatically sent by the system.\n" +
                        "If you have any question, welcome to contact DQMS Team.\n" +
                        "\n" +
                        "Best Regard\n" +
                        "DQMS Software Developement Requirement System Administrator <dqms_admin@wistron.com>"
                    )
                    sender = ""
                    developers = order.developers
                    developer_list = []
                    if 'contactor' in developers:
                        developer_list.append(developers['contactor'])
                    if 'member' in developers:
                        developer_list.extend(developers['member'])
                    developer_mail_list = list(Employee.objects.using('hr').filter(
                        employee_id__in=developer_list).values_list('mail', flat=True))
                    recipient_list = developer_mail_list
                    send_mail(email_subject, email_message, sender, recipient_list)
                elif direction_flag == "Close":
                    # Debug Code
                    debug_message = (
                        f"Order Status:'{order_status}', direction_flag:'{direction_flag}'"
                    )
                    logger.debug(debug_message)
                    order.form_end_time = timezone.now()
                    order.status = {
                        "P5": {
                            "initiator": "Close"
                        }
                    }
                    order.save()
                    # Send email to all member
                    email_subject = "<Close> There is a software development closed order"
                    email_message = (
                        "Dear all,\n" +
                        "\n" +
                        "There is a software developement closed order.\n" +
                        "You can click below link to check the order detail.\n" +
                        f"{self.request.build_absolute_uri(location='/')}?order={order.id} \n" +
                        "\n" +
                        "Don't reply this mail as it is automatically sent by the system.\n" +
                        "If you have any question, welcome to contact DQMS Team.\n" +
                        "\n" +
                        "Best Regard\n" +
                        "DQMS Software Developement Requirement System Administrator <dqms_admin@wistron.com>"
                    )
                    sender = ""
                    # Collect all member mail in recipient_list
                    signer_id_list = list(order.signature_set.order_by(
                        'signer').distinct('signer').values_list('signer', flat=True))
                    signer_mail_list = list(Employee.objects.using('hr').filter(
                        employee_id__in=signer_id_list).values_list('mail', flat=True))

                    developers = order.developers
                    developer_list = []
                    if 'contactor' in developers:
                        developer_list.append(developers['contactor'])
                    if 'member' in developers:
                        developer_list.extend(developers['member'])

                    developer_mail_list = list(Employee.objects.using('hr').filter(
                        employee_id__in=developer_list).values_list('mail', flat=True))

                    recipient_list = [
                        Employee.objects.using('hr').get(employee_id=order.assigner).mail,
                        Employee.objects.using('hr').get(employee_id=order.initiator).mail,
                    ]
                    recipient_list.extend(
                        [mail for mail in signer_mail_list if mail not in recipient_list]
                    )
                    recipient_list.extend(
                        [mail for mail in developer_mail_list if mail not in recipient_list]
                    )
                    send_mail(email_subject, email_message, sender, recipient_list)
            else:
                error_message = (
                    f"The status of order id '{order_id}' is not correct. " +
                    "There are not correct direction_flag attribure in order status."
                )
                logger.error(error_message)

        # TODO Send notification to all member


class SignatureViewSet(QueryDataMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
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
        serializer.save()
        signature_id = serializer.data['id']
        signature = Signature.objects.get(pk=signature_id)
        signature_status = signature.status
        order = Order.objects.get(pk=signature.order.id)
        order_copy = Order.objects.get(pk=signature.order.id)

        # Create History (including last record and update content with json)
        last_order_tracker = dict(OrderTracker.objects.filter(order=order.id).order_by('created_time').values()[0])
        del last_order_tracker['order_id']
        kwargs = {}
        kwargs['context'] = {'accounts': cache.get('accounts', None)}
        kwargs['context'].update({'projects': cache.get('projects', None)})
        kwargs['context'].update({'employees': cache.get('employees', None)})

        comment = {
            'last_order': OrderDynamicSerializer(last_order_tracker, **kwargs).data,
            'update_content': OrderDynamicSerializer(order_copy, **kwargs).data,
        }

        history = {
            'editor': 'system',
            'comment': json.dumps(comment),
            'order': order
        }
        History.objects.create(**history)

        # Save to OrderTracker
        order_tracker_serializer = OrderTrackerSerializer(data=model_to_dict(order))
        if order_tracker_serializer.is_valid(raise_exception=True):
            order_tracker_serializer.save(order=order, form_begin_time=order.form_begin_time)

        logger.debug(f"Origin Signature Stauts: {signature_status}, Origin Order Status: {order.status}")
        signer = signature.signer
        developers = order.developers
        if signature_status == 'Approve':
            signer_department_id = Employee.objects.using('hr').get(employee_id__iexact=signer).department_id
            # Check signature stage is finished or not. The last signer will be function head leader.
            # Stop Condiontion is that Consecutive occurrences times of the zero in department_id are
            # greater/equal four times.
            count = 0
            for char in signer_department_id[::-1]:
                if char == '0':
                    count += 1
                elif char != '0':
                    break

            if 'P1' in order.status:
                if count >= 4:
                    order.status = {
                        'P2': {
                            'assigner': ''
                        }
                    }
                    order.save()
                    # TODO Send email to assigner
                    email_subject = "<Confirm> There is a software development order waiting your confirm."
                    recipient_name = Employee.objects.using('hr').get(employee_id=order.assigner).english_name.title()
                    email_message = (
                        f"Dear {recipient_name},\n" +
                        "\n" +
                        "There is a software developement order that is waiting for your response.\n" +
                        "You can click below link to check the order detail.\n" +
                        f"{self.request.build_absolute_uri(location='/')}?order={order.id} \n"
                        "\n" +
                        "Don't reply this mail as it is automatically sent by the system.\n" +
                        "If you have any question, welcome to contact DQMS Team.\n" +
                        "\n" +
                        "Best Regard\n" +
                        "DQMS Software Developement Requirement System Administrator <dqms_admin@wistron.com>"
                    )
                    sender = ""
                    recipient_list = [Employee.objects.using('hr').get(employee_id=order.assigner).mail]
                    send_mail(email_subject, email_message, sender, recipient_list)
                elif count < 4:
                    # Find next signer
                    non_zero_part = len(signer_department_id) - count - 1
                    next_signer_department_id = signer_department_id[:non_zero_part] + '0' * (count + 1)
                    status, result = self.get_department_via_query(department_id=next_signer_department_id)
                    if not (status and result):
                        warn_message = (
                            f"It couldn't be find next signer with the current signer '{signer}'"
                        )
                        logger.warning(warn_message)
                        return
                    if next_signer_department_id in result:
                        next_signer = result[next_signer_department_id].get('dm', None)

                    # Order Status Change
                    order.status = {
                        'P1': {
                            next_signer: ''
                        },
                    }
                    order.save()
                    # Check whether craete next signature
                    max_sequence = order.signature_set.aggregate(Max('sequence'))['sequence__max']
                    if order.signature_set.get(sequence=max_sequence).status == 'Approve':

                        # Create next signature
                        next_signature = {
                            'sequence': max_sequence + 1,
                            'signer': next_signer,
                            'sign_unit': next_signer_department_id,
                            'status': '',
                            'comment': '',
                            'role_group': signature.role_group,
                            'order': order
                        }
                        Signature.objects.create(**next_signature)
                        # Send Email to next signer
                        email_subject = "<Signing> There is a software development order waiting your signing"
                        recipient_name = Employee.objects.using('hr').get(employee_id=next_signer).english_name.title()
                        email_message = (
                            f"Dear {recipient_name},\n" +
                            "\n" +
                            "There is a software developement order that is waiting for your signing.\n" +
                            "You can click below link to check the order detail.\n" +
                            f"{self.request.build_absolute_uri(location='/')}?order={order.id} \n"
                            "\n" +
                            "Don't reply this mail as it is automatically sent by the system.\n" +
                            "If you have any question, welcome to contact DQMS Team.\n" +
                            "\n" +
                            "Best Regard\n" +
                            "DQMS Software Developement Requirement System Administrator <dqms_admin@wistron.com>"
                        )
                        sender = ""
                        recipient_list = [Employee.objects.using('hr').get(employee_id=next_signer)]
                        send_mail(email_subject, email_message, sender, recipient_list)
            elif 'P4' in order.status:
                if count >= 4:
                    order.status = {
                        'P5': {
                            'developers': ''
                        }
                    }
                    order.save()
                    # TODO Send email to developers
                    email_subject = "<Confirm> There is a software development order waiting your confirm."
                    recipient_name = Employee.objects.using('hr').get(
                        employee_id=order.developers['contactor']).english_name.title()
                    email_message = (
                        f"Dear {recipient_name} & developers,\n" +
                        "\n" +
                        "There is a software developement order that is waiting for your response.\n" +
                        "You can click below link to check the order detail.\n" +
                        f"{self.request.build_absolute_uri(location='/')}?order={order.id} \n"
                        "\n" +
                        "Don't reply this mail as it is automatically sent by the system.\n" +
                        "If you have any question, welcome to contact DQMS Team.\n" +
                        "\n" +
                        "Best Regard\n" +
                        "DQMS Software Developement Requirement System Administrator <dqms_admin@wistron.com>"
                    )
                    sender = ""
                    developers = order.developers
                    developer_list = []
                    if 'contactor' in developers:
                        developer_list.append(developers['contactor'])
                    if 'member' in developers:
                        developer_list.append(developers['member'])
                    developer_mail_list = list(Employee.objects.using('hr').get(
                        employee_id__in=developer_list).distinct('mail').value_list('mail', flat=True))
                    recipient_list = developer_mail_list
                    send_mail(email_subject, email_message, sender, recipient_list)
                elif count < 4:
                    # Find next signer
                    non_zero_part = len(signer_department_id) - count - 1
                    next_signer_department_id = signer_department_id[:non_zero_part] + '0' * (count + 1)
                    status, result = self.get_department_via_query(department_id=next_signer_department_id)
                    if not (status and result):
                        warn_message = (
                            f"It couldn't be find next signer with the current signer '{signer}'"
                        )
                        logger.warning(warn_message)
                        return
                    if next_signer_department_id in result:
                        next_signer = result[next_signer_department_id].get('dm', None)
                    # Order Status Change
                    order.status = {
                        'P4': {
                            next_signer: ''
                        },
                    }
                    order.save()
                    # Check whether craete next signature
                    max_sequence = order.signature_set.aggregate(Max('sequence'))['sequence__max']
                    if order.signature_set.get(sequence=max_sequence).status == 'Approve':

                        # Create next signature
                        next_signature = {
                            'sequence': max_sequence + 1,
                            'signer': next_signer,
                            'sign_unit': next_signer_department_id,
                            'status': '',
                            'comment': '',
                            'role_group': signature.role_group,
                            'order': order
                        }
                        Signature.objects.create(**next_signature)
                        # TODO Send email to next signer
                        email_subject = "<Signing> There is a software development order waiting your signing"
                        recipient_name = Employee.objects.using('hr').get(employee_id=next_signer).english_name.title()
                        email_message = (
                            f"Dear {recipient_name},\n" +
                            "\n" +
                            "There is a software developement order that is waiting for your signing.\n" +
                            "You can click below link to check the order detail.\n" +
                            f"{self.request.build_absolute_uri(location='/')}?order={order.id} \n"
                            "\n" +
                            "Don't reply this mail as it is automatically sent by the system.\n" +
                            "If you have any question, welcome to contact DQMS Team.\n" +
                            "\n" +
                            "Best Regard\n" +
                            "DQMS Software Developement Requirement System Administrator <dqms_admin@wistron.com>"
                        )
                        sender = ""
                        recipient_list = [Employee.objects.using('hr').get(employee_id=next_signer).mail]
                        send_mail(email_subject, email_message, sender, recipient_list)
        elif signature_status == 'Return':
            if 'P1' in order.status:
                order.status = {
                    'P0': {
                        'initiator': ''
                    },
                    'signed': False
                }
                order.save()
                # TODO Send email to initiator
                email_subject = "<Return> There is a software development return order waiting your confirm."
                recipient_name = Employee.objects.using('hr').get(employee_id=order.initiator).english_name.title()
                email_message = (
                    f"Dear {recipient_name},\n" +
                    "\n" +
                    "There is a software developement return order that is waiting for your response.\n" +
                    "You can click below link to check the order detail.\n" +
                    f"{self.request.build_absolute_uri(location='/')}?order={order.id} \n"
                    "\n" +
                    "Don't reply this mail as it is automatically sent by the system.\n" +
                    "If you have any question, welcome to contact DQMS Team.\n" +
                    "\n" +
                    "Best Regard\n" +
                    "DQMS Software Developement Requirement System Administrator <dqms_admin@wistron.com>"
                )
                sender = ""
                recipient_list = [Employee.objects.using('hr').get(employee_id=order.initiator).mail]
                send_mail(email_subject, email_message, sender, recipient_list)
            elif 'P4' in order.status:
                order.status = {
                    'P3': {
                        'initiator': '',
                        'assigner': '',
                        'developers': ''
                    },
                    'signed': False
                }
                order.save()
                # TODO Send email to assigner
                email_subject = "<Reschedule> There is a software development order waiting your reschedule"
                recipient_name = Employee.objects.using('hr').get(employee_id=order.assigner).english_name.title()
                email_message = (
                    f"Dear {recipient_name},\n" +
                    "\n" +
                    "There is a software developement return order that is waiting for your reschedule.\n" +
                    "You can click below link to check the order detail.\n" +
                    f"{self.request.build_absolute_uri(location='/')}?order={order.id} \n"
                    "\n" +
                    "Don't reply this mail as it is automatically sent by the system.\n" +
                    "If you have any question, welcome to contact DQMS Team.\n" +
                    "\n" +
                    "Best Regard\n" +
                    "DQMS Software Developement Requirement System Administrator <dqms_admin@wistron.com>"
                )
                sender = ""
                recipient_list = [Employee.objects.using('hr').get(employee_id=order.assigner).mail]
                send_mail(email_subject, email_message, sender, recipient_list)
        elif signature_status == 'Close':
            if 'P1' in order.status:
                order.status = {
                    'P1': {
                        signer: 'Close'
                    }
                }
                order.form_end_time = timezone.now()
                order.save()
            elif 'P4' in order.status:
                order.status = {
                    'P4': {
                        signer: 'Close'
                    }
                }
                order.form_end_time = timezone.now()
                order.save()
            # TODO Send email to all member
            email_subject = "<Close> There is a software development closed order"
            email_message = (
                "Dear all,\n" +
                "\n" +
                "There is a software developement closed order.\n" +
                "You can click below link to check the order detail.\n" +
                f"{self.request.build_absolute_uri(location='/')}?order={order.id} \n" +
                "\n" +
                "Don't reply this mail as it is automatically sent by the system.\n" +
                "If you have any question, welcome to contact DQMS Team.\n" +
                "\n" +
                "Best Regard\n" +
                "DQMS Software Developement Requirement System Administrator <dqms_admin@wistron.com>"
            )
            sender = ""
            # Collect all member mail in recipient_list
            signer_id_list = list(order.signature_set.order_by(
                'signer').distinct('signer').values_list('signer', flat=True))
            signer_mail_list = list(Employee.objects.using('hr').filter(
                employee_id__in=signer_id_list).values_list('mail', flat=True))

            developer_list = []
            if 'contactor' in developers:
                developer_list.append(developers['contactor'])
            if 'member' in developers:
                developer_list.extend(developers['member'])

            developer_mail_list = list(Employee.objects.using('hr').filter(
                employee_id__in=developer_list).values_list('mail', flat=True))

            recipient_list = [
                Employee.objects.using('hr').get(employee_id=order.assigner).mail,
                Employee.objects.using('hr').get(employee_id=order.initiator).mail,
            ]
            recipient_list.extend(
                [mail for mail in signer_mail_list if mail not in recipient_list]
            )
            recipient_list.extend(
                [mail for mail in developer_mail_list if mail not in recipient_list]
            )
            send_mail(email_subject, email_message, sender, recipient_list)
        # TODO Send notification to all member
