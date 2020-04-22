""" singature app's api viewsets.py """
import logging

from develop_requirement_proj.utils.mixins import QueryDataMixin

from rest_framework import mixins, viewsets

from ..models import Account, Project
# from .filters import ProjectFilter
from .serializers import AccountSerializer, ProjectSerializer

logger = logging.getLogger(__name__)


class AccountViewSet(QueryDataMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """ Provide Account resource with `list` action """
    serializer_class = AccountSerializer

    def get_queryset(self):
        """ Get queryset from TeamRoster 2.0 System """
        queryset = []
        status, results = self.get_account_via_search()
        if status and results:
            queryset = [Account(**result) for result in results]

        return queryset


class ProjectViewSet(QueryDataMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """ Provide Porject resource from Account Project System """
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = []
        params = self.request.query_params.dict()
        status, results = self.get_project_via_search(**params)
        if status and results:
            queryset = [Project(**result) for result in results]

        return queryset
