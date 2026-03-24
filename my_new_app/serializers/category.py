from rest_framework import serializers

from my_new_app.models import Category
from typing import Any


class CategoryCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['name', 'description']


    def create(self, validated_data: dict[str, Any]) -> Category:
        category_name = validated_data.get('name')
        if Category.objects.filter(name=category_name).exists():
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