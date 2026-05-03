from rest_framework.decorators import action
from django.db.models import Count
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from my_new_app.models import Category
from my_new_app.serializers import CategoryCreateSerializer



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.filter(is_deleted=False)
    serializer_class = CategoryCreateSerializer
    permission_classes = [AllowAny]

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
