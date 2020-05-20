""" singature app's api viewsets.py """
import logging

from develop_requirement_proj.employee.models import Employee
from develop_requirement_proj.utils.mixins import QueryDataMixin
from employee.api.serializers import EmployeeSerializer

from rest_framework import mixins, serializers, views, viewsets
from rest_framework.response import Response

from ..models import Account, Document, Project
# from .filters import ProjectFilter
from .serializers import (
    AccountSerializer, DocumentSerializer, ProjectSerializer,
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
