from rest_framework import serializers
from my_new_app.models import Task
from django.utils import timezone
from .subtask import SubTaskSerializer


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Task
        fields = ['id','title', 'description', 'status', 'deadline', 'owner']


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Task
        fields = [
                  'id',
                  'title',
                  'description',
                  'status',
                  'deadline',
                  'subtasks',
                   'owner'
                  ]


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline']
        validators = []

    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Deadline cannot be in the past.")
        return value