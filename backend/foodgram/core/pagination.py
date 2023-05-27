from rest_framework.pagination import PageNumberPagination
from django.conf import settings


class LargeResultsSetPagination(PageNumberPagination):
    page_size = settings.PAGE_SIZE
    page_size_query_param = 'page_size'
