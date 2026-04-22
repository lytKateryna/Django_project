from rest_framework.pagination import CursorPagination


class MyCustomCursorPagination(CursorPagination):
    page_size = 5
    ordering = '-id'

