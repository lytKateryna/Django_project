"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from my_new_app.views import index, homepage
from my_new_app.views import tasks
from my_new_app.views import task_id
from my_new_app.views import task_statistic

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('page/', homepage),
    path('tasks/', tasks),
    path('tasks/<int:task_id>', task_id),
    path('tasks/statistic/', task_statistic),
]

