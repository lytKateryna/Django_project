from rest_framework import serializers
from django.utils import timezone
from my_new_app.models import SubTask




class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'status']


class SubTaskCreateSerializer(serializers.ModelSerializer):
    # created_at = serializers.DateTimeField(read_only=True)
    created_at = serializers.HiddenField(default=timezone.now)
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'status', 'created_at', 'task', 'deadline']