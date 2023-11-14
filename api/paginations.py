from rest_framework.pagination import LimitOffsetPagination

class MyOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 1000000000000000000000000000000000000000000000000000000000000


class OffsetPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 1000000000000000000000000000000000000000000000000000000000000
