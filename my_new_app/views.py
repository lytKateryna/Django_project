from calendar import day_name

from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.http import HttpResponse
from my_new_app.serializers.task import TaskSerializer, TaskCreateSerializer, TaskDetailSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from my_new_app.models import Task
from rest_framework import status
from django.db.models import Count
from django.utils import timezone
from my_new_app.models import SubTask
from my_new_app.serializers.subtask import SubTaskSerializer, SubTaskCreateSerializer
from django.db.models.functions import ExtractWeekDay
from rest_framework.pagination import PageNumberPagination


# Create your views here.
def index(request):
    return HttpResponse(
        '<h1>Hello Kateryna!</h1>'
    )

def homepage(request):
    return HttpResponse(
        '<h1>My Homepage!!!</h1>'
    )


class TasksListAPIView(APIView):
    def get_tasks(self):
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

    def get(self, request: Response, *args, **kwargs):
        try:
            tasks = self.get_tasks()

        except ValueError as e:
            return Response(
                {"error": "Invalid day"}, status=400
            )

        serializer = TaskSerializer(tasks, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK)

@api_view(['POST', 'GET'])
def tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.all()

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        raw_data = request.data
        serializer = TaskSerializer(data=raw_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def task_id(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error":"Task not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskDetailSerializer(task)
    return Response(serializer.data)

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


class SubTaskListCreateView(APIView, PageNumberPagination):
    page_size = 5

    def get_page_size(self, request:Response):
        page_size = request.query_params.get('page_size')

        if page_size and page_size.isdigit():
            return int(page_size)
        return self.page_size


    def get(self, request):
        subtasks = SubTask.objects.all().order_by('created_at')

        task_title = request.query_params.get('task')
        status_value = request.query_params.get('status')

        if task_title:
            subtasks = subtasks.filter(task__title__icontains=task_title)
        if status_value:
            subtasks = subtasks.filter(status=status_value)

        page_size = self.get_page_size(request)
        self.page_size = page_size
        results = self.paginate_queryset(
            queryset=subtasks,
            request=request,
            view=self
        )

        serializer = SubTaskSerializer(results, many=True)
        return self.get_paginated_response(data=serializer.data)


    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):

    def get(self, request, pk):
        try:
            subtask = SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return Response({"error": "Subtask not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            subtask = SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return Response({"error":"Subtask not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        try:
            subtask = SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return Response({"error":"Subtask not found"}, status=status.HTTP_404_NOT_FOUND)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

