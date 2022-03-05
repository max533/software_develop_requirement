import logging

from rest_framework import pagination

logger = logging.getLogger(__name__)


class OrderPagination(pagination.PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 50
