from django.http import HttpResponse
from django.db.models import Count
from django.utils import timezone

from rest_framework import filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from django_filters.rest_framework import DjangoFilterBackend
from my_new_app.models import Task, SubTask, Category
from my_new_app.serializers.task import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskDetailSerializer
)
from my_new_app.serializers.subtask import (
    SubTaskSerializer,
    SubTaskCreateSerializer
)
from my_new_app.serializers.category import (
    CategoryCreateSerializer,
)
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import (
    GenericViewSet,
    ModelViewSet,
    ReadOnlyModelViewSet
)


# Create your views here.
def index(request):
    return HttpResponse(
        '<h1>Hello Kateryna!</h1>'
    )


def homepage(request):
    return HttpResponse(
        '<h1>My Homepage!!!</h1>'
    )


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.filter(is_deleted=False)
    serializer_class = CategoryCreateSerializer


    @action(methods=['GET'], detail=False)
    def get_count_tasks(self, request, *args, **kwargs):
        queryset = self.get_queryset().annotate(
            count_tasks=Count('tasks')
        )
        serializer = self.get_serializer(queryset, many=True)

        return Response(data={
            "total_objects": self.get_queryset().count(),
            "results": serializer.data
            },
            status=status.HTTP_200_OK
        )


class TasksListCreateGenericView(ListCreateAPIView):
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskSerializer

    def get_queryset(self):
        tasks = Task.objects.all()
        day = self.request.query_params.get('day')
        if day:
            day = day.strip().lower()
            weekdays = {
                'monday': 2,
                'tuesday': 3,
                'wednesday': 4,
                'thursday': 5,
                'friday': 6,
                'saturday': 7,
                'sunday': 1
            }
            if day not in weekdays:
                raise ValueError("Invalid day")

            tasks = tasks.filter(deadline__week_day=weekdays[day])

        return tasks


class TaskRetrieveUpdateDestroyGenericView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TaskCreateSerializer
        return TaskDetailSerializer


@api_view(['GET'])
def task_statistic(request):
    total_tasks = Task.objects.count()

    status_counts_qs = (
        Task.objects
        .values('status')
        .annotate(count=Count('id'))
    )

    status_counts = {
        item['status']: item['count']
        for item in status_counts_qs
    }

    deadline_tasks = Task.objects.filter(
        deadline__lt=timezone.now()
    ).exclude(status='closed').count()

    data = {
        "total_tasks": total_tasks,
        "tasks_by_status": status_counts,
        "deadline_tasks": deadline_tasks
    }

    return Response(data, status=status.HTTP_200_OK)


class SubTaskPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'


class SubTaskListCreateGenericView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    pagination_class = SubTaskPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubTaskCreateSerializer
        return SubTaskSerializer


class SubTaskRetrieveUpdateDestroyGenericView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return SubTaskCreateSerializer
        return SubTaskSerializer
