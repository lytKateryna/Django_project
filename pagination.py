from rest_framework.pagination import CursorPagination


class MyCustomCursorPagination(CursorPagination):
    page_size = 6
    ordering = '-id'

