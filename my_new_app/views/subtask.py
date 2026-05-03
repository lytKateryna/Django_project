from rest_framework import filters

from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from my_new_app.models import SubTask
from my_new_app.serializers.subtask import (
    SubTaskSerializer,
    SubTaskCreateSerializer
)
from my_new_app.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


class SubTaskPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'


class SubTaskListCreateGenericView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = SubTaskSerializer
    pagination_class = SubTaskPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['-created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubTaskCreateSerializer
        return SubTaskSerializer

    def get_queryset(self):
        return SubTask.objects.filter(task__owner=self.request.user)

    def perform_create(self, serializer):
        task = serializer.validated_data.get('task')

        if task.owner != self.request.user:
            raise PermissionDenied("Нельзя создать подзадачу для чужой задачи.")

        serializer.save()


class SubTaskRetrieveUpdateDestroyGenericView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    lookup_field = 'id'

    def get_queryset(self):
        return SubTask.objects.filter(task__owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return SubTaskCreateSerializer
        return SubTaskSerializer
