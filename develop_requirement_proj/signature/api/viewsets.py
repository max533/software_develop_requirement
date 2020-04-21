""" singature app's api viewsets.py """
from develop_requirement_proj.utils.mixins import QueryDataMixin

from rest_framework import mixins, viewsets

from ..models import Account
from .serializers import AccountSerializer


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
