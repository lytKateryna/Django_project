from django.contrib import admin
from my_new_app.models import Task, Category, SubTask


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    list_filter = ['name']
    list_per_page = 2


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'categories','status', 'deadline']
    search_fields = ['title']
    list_filter = ['status', 'categories']
    list_editable = ["status"]
    list_per_page = 2

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'task','status', 'deadline']
    search_fields = ['title']
    list_filter = ['task', 'status']
    list_editable = ["status"]
    list_per_page = 2


