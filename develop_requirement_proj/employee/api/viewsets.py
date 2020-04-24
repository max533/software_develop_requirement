""" Employee app's api viewsets.py """
import logging

from develop_requirement_proj.utils.mixins import QueryDataMixin
from django_filters import rest_framework as filters

from django.shortcuts import get_object_or_404

from rest_framework import mixins, response, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Employee
from .filters import EmployeeFilter
from .paginations import EmployeePagination
from .serializers import EmployeeSerializer

logger = logging.getLogger(__name__)


class EmployeeViewSet(QueryDataMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Employee.objects.using('hr').all()
    serializer_class = EmployeeSerializer
    pagination_class = EmployeePagination
    filter_backends = [filters.DjangoFilterBackend]
    filter_class = EmployeeFilter

    def get_object(self):
        """
        Provide object and check object permission for `list` and `current_user` action
        """
        queryset = self.filter_queryset(self.get_queryset())
        if self.action == 'current_user':
            obj = get_object_or_404(queryset, employee_id=self.request.user.username)
        else:
            # Perform the lookup filtering.
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
            assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
            )

            filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
            obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def get_paginated_response(self, data):
        """
        Adjust the pagination's response to fit bootstrap4 server-side search
        """
        assert self.paginator is not None
        return response.Response(
            {
                'rows': data,
                'total': self.paginator.page.paginator.count,
                'totalNotFilter': len(self.queryset),
            }
        )

    @action(detail=False, methods=['GET'], url_path='me', url_name='current-user')
    def current_user(self, request, *args, **kwargs):
        """ Return the current user information """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
