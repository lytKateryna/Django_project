from django.contrib import admin
from my_new_app.models import Task, Category, SubTask


# Register your models here.


admin.site.register(Category)
admin.site.register(Task)
admin.site.register(SubTask)