from rest_framework import serializers

from my_new_app.models import Category
from typing import Any

from my_new_app.serializers import TaskSerializer


class CategoryCreateSerializer(serializers.ModelSerializer):
    count_tasks = serializers.IntegerField(
        required=False,
        read_only=True
    )
    class Meta:
        model = Category
        fields = [
            'name', 
            'description',
            'count_tasks',
            'is_deleted'
        ]


    def create(self, validated_data: dict[str, Any]) -> Category:
        category_name = validated_data.get('name')
        if Category.objects.filter(name__iexact=category_name).exists():
            raise serializers.ValidationError("Category with this name already exists.")
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        category_name = validated_data.get('name', instance.name)
        if Category.objects.filter(name=category_name).exclude(id=instance.id).exists():
            raise serializers.ValidationError("Category with this name already exists.")
        instance.name = category_name
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        return instance
"""
        for attr, value in validated_data.items():  (метод не зависит от название полей)
            setattr(instance, attr, value)
            instance.save()
            return instance
"""
