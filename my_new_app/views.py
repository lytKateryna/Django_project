from django.http import HttpResponse
from my_new_app.serializers.task import TaskSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from my_new_app.models import Task
from rest_framework import status
from django.db.models import Count
from django.utils import timezone



# Create your views here.
def index(request):
    return HttpResponse(
        '<h1>Hello Kateryna!</h1>'
    )

def homepage(request):
    return HttpResponse(
        '<h1>My Homepage!!!</h1>'
    )


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

    serializer = TaskSerializer(task)
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
    ).count()

    data = {
        "total_tasks": total_tasks,
        "tasks_by_status": status_counts,
        "deadline_tasks": deadline_tasks
    }

    return Response(data, status=status.HTTP_200_OK)


