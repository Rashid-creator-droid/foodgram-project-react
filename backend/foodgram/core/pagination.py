from rest_framework import pagination
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10