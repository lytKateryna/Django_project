from rest_framework import serializers
from django.utils import timezone
from my_new_app.models import SubTask




class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'status']


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    # created_at = serializers.HiddenField(default=timezone.now)
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'status', 'created_at', 'task', 'deadline']

        validators = []
        def validate(self, attrs):
            title = attrs.get('title')
            created_at = self.instance.created_at

            if title is not None:
                title = self.instance.title

            qs = SubTask.objects.filter(
                title__icontains=title,
                created_at__date=created_at,).exclude(id=self.instance.pk)

            if qs.exists():
                raise serializers.ValidationError('Subtask with this title already exists')

            return attrs

