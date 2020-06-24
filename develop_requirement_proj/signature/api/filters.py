import json
import logging

from django_filters import rest_framework as filters

from rest_framework import exceptions

from ..models import Order

logger = logging.getLogger(__name__)


class OrderFilterBackend(filters.DjangoFilterBackend):
    """ """
    def get_filterset_kwargs(self, request, queryset, view):
        kwargs = super().get_filterset_kwargs(request, queryset, view)

        # Transform Bootstrap-Table filter's style to django-filter query string filter's style
        # Ex/ filter={'titile':'abc'} --> title=abc
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
                kwarg_data.update(query_string)
                kwargs['data'] = kwarg_data

        return kwargs


class OrderFilter(filters.FilterSet):

    assigner = filters.CharFilter(field_name='assigner__display_name', lookup_expr='icontains')
    initiator = filters.CharFilter(field_name='initiator__employee_id', lookup_expr='icontains')
    form_begin_time = filters.IsoDateTimeFromToRangeFilter()

    class Meta:
        model = Order
        fields = {
            'id': ['exact'],
            'account': ['exact'],
            'project': ['exact'],
            'title': ['icontains'],
            'parent': ['exact'],
        }
