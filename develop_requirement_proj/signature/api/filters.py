import ast
import json
import logging

from develop_requirement_proj.employee.models import Employee
from django_filters import rest_framework as filters, utils

from django.db.models import Q

from rest_framework import exceptions

from ..models import Order

logger = logging.getLogger(__name__)


class OrderFilterBackend(filters.DjangoFilterBackend):
    """ """
    def get_filterset_kwargs(self, request, queryset, view):
        kwargs = super().get_filterset_kwargs(request, queryset, view)

        # Transform Bootstrap-Table filter's style to django-filter query string filter's style
        # Ex/ filter='{"title":"abc"}' --> filter={"title":"abc"}
        if 'filter' in request.query_params:
            if request.query_params['filter']:
                kwarg_data = kwargs['data'].copy()

                del kwarg_data['filter']
                try:
                    query_string = json.loads(request.query_params['filter'])
                except json.decoder.JSONDecodeError as err:
                    error_message = f"Query string format is incorrect. Error Message : {err}"
                    logger.debug(error_message)
                    raise exceptions.ParseError

                # Convert english name into employee_id with initiator, assigner, developers field
                # TODO Using serialzier validate query will be clear and better
                if 'initiator' in query_string:
                    initiator = query_string.get('initiator').strip()
                    if initiator:
                        initiator_employee_id = Employee.objects.using('hr').filter(
                            english_name__icontains=initiator).values_list('employee_id', flat=True)
                        query_string['initiator'] = list(initiator_employee_id)
                    else:
                        del query_string['initiator']

                if 'assigner' in query_string:
                    assigner = query_string.get('assigner').strip()
                    if assigner:
                        assigner_employee_id = Employee.objects.using('hr').filter(
                            english_name__icontains=assigner).values_list('employee_id', flat=True)
                        query_string['assigner'] = list(assigner_employee_id)
                    else:
                        del query_string['assigner']

                if 'developers' in query_string:
                    developers = query_string.get('developers').strip()
                    if developers:
                        developers_employee_id = Employee.objects.using('hr').filter(
                            english_name__icontains=developers).values_list('employee_id', flat=True)
                        query_string['developers'] = list(developers_employee_id)
                    else:
                        del query_string['developers']

                kwarg_data.update(query_string)
                kwargs['data'] = kwarg_data

        return kwargs

    def filter_queryset(self, request, queryset, view):
        filterset = self.get_filterset(request, queryset, view)
        if filterset is None:
            return queryset

        # If there are not any query user in hr database, it will return empty queryset
        for query_item in ['initiator', 'assigner', 'developers']:
            if query_item in filterset.data:
                query_value = filterset.data[query_item]
                if not query_value:
                    return Order.objects.none()

        if not filterset.is_valid() and self.raise_exception:
            raise utils.translate_validation(filterset.errors)
        return filterset.qs


class OrderFilter(filters.FilterSet):

    initiator = filters.CharFilter(method='initiator_filter')
    assigner = filters.CharFilter(method='assigner_filter')
    developers = filters.CharFilter(method='developers_filter')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')
    form_begin_time = filters.IsoDateTimeFromToRangeFilter()

    class Meta:
        model = Order
        fields = {
            'id': ['exact'],
            'account': ['exact'],
            'project': ['exact'],
            'parent': ['exact'],
        }

    def initiator_filter(self, queryset, name, value):
        lookup = '__'.join([name, 'in'])
        print(123)
        return queryset.filter(**{lookup: ast.literal_eval(value)})

    def assigner_filter(self, queryset, name, value):
        print(123)
        lookup = '__'.join([name, 'in'])
        return queryset.filter(**{lookup: ast.literal_eval(value)})

    def developers_filter(self, queryset, name, value):
        print(123)
        lookup_contactor = '__'.join([name, 'contactor', 'contained_by'])
        lookup_member = '__'.join([name, 'member', 'contained_by'])
        value = ast.literal_eval(value)
        complex_lookup = Q(**{lookup_contactor: value}) | Q(**{lookup_member: value})
        return queryset.filter(complex_lookup)
