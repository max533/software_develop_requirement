""" singature app's api viewsets.py """
import logging

from develop_requirement_proj.utils.mixins import QueryDataMixin

from rest_framework import mixins, views, viewsets
from rest_framework.response import Response

from ..models import Account, Project
# from .filters import ProjectFilter
from .serializers import AccountSerializer, ProjectSerializer

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
