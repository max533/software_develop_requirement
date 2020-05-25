""" singature app's api viewsets.py """
import logging
import time

from develop_requirement_proj.employee.models import Employee
from develop_requirement_proj.utils.mixins import QueryDataMixin
from employee.api.serializers import EmployeeSerializer

from django.core.cache import cache
from django.db.models import Max

from rest_framework import mixins, serializers, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import (
    Account, Document, ProgressTracker, Project, Schedule, ScheduleTracker,
)
# from .filters import ProjectFilter
from .serializers import (
    AccountSerializer, DocumentSerializer, EmployeeNonModelSerializer,
    ProgressSerializer, ProjectSerializer, ScheduleSerializer,
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
    """ Provide Project resource from Account Project System """
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

        return Response(final_result)


class AssginerViewSet(QueryDataMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """ Provide Assigner resource by project_id and sub_function """
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
    """ Provide Document resource by order_id """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get_queryset(self):
        queryset = self.queryset
        order_id = self.request.query_params.get("order_id", None)
        if order_id is not None:
            queryset = queryset.filter(order=order_id)
        return queryset


class ScheduleViewSet(viewsets.ModelViewSet):
    """ Provide Schedule resource by order_id """
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
        return Response(result)

    def perform_create(self, serializer):
        """
        After creating new schedule, it will record the current schedule
        with same version in `ScheduleTracker` table.
        """
        serializer.save()
        # Update `Schedule` current version which filter by order_id
        objs = Schedule.objects.filter(order=serializer.data['order'])
        for obj in objs:
            obj.version += 1
        Schedule.objects.bulk_update(objs, ['version'])
        # Create `Schedule` history and set primary key for `ScheduleTracker` Table
        result = ScheduleTracker.objects.aggregate(Max('id'))
        count = result['id__max'] if result['id__max'] is not None else 0
        for obj in objs:
            count += 1
            obj.id = count
        ScheduleTracker.objects.bulk_create(objs)

    def perform_update(self, serializer):
        """
        After updating new schedule, it will record the current schedule
        with same version in `ScheduleTracker` table.
        """
        serializer.save()
        # Update `Schedule` currnet version which filter by order_id
        objs = Schedule.objects.filter(order=serializer.data['order'])
        for obj in objs:
            obj.version += 1
        Schedule.objects.bulk_update(objs, ['version'])
        # Create `Schedule` history and set primary key for `ScheduleTracker` Table
        result = ScheduleTracker.objects.aggregate(Max('id'))
        count = result['id__max'] if result['id__max'] is not None else 0
        for obj in objs:
            count += 1
            obj.id = count
        ScheduleTracker.objects.bulk_create(objs)

    def perform_destroy(self, instance):
        """
        After deleting new schedule, it will record the current schedule
        with same version in `ScheduleTracker` table.
        """
        # Update `Schedule` currnet version which filter by order_id
        objs = Schedule.objects.filter(order=instance.order)
        for obj in objs:
            obj.version += 1
        Schedule.objects.bulk_update(objs, ['version'])
        # Delete instance
        instance.delete()
        # Create `Schedule` history and set primary key for `ScheduleTracker` Table
        result = ScheduleTracker.objects.aggregate(Max('id'))
        count = result['id__max'] if result['id__max'] is not None else 0
        for obj in objs:
            count += 1
            obj.id = count
        ScheduleTracker.objects.bulk_create(objs)


class ProgressViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ Provide Development Progress Resource with `list` and `create` action. """
    queryset = ProgressTracker.objects.all()
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
            cache.set('employees', objects, 60 * 60 * 24)
        context['employee'] = objects
        return context
