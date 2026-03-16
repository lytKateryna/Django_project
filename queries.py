import os
import django
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup()

from my_new_app.models import Category, Task, SubTask

Task.objects.filter(title="Prepare presentation").delete()

print("Create")
task, created = Task.objects.get_or_create(
    title = "Prepare presentation",
    description = "Prepare materials and slides for the presentation",
    status = "new",
    deadline = timezone.now() + timedelta(days=3),
)

category = Category.objects.get(name="Срочные")

task.categories.set([category])

subtask1, created = SubTask.objects.get_or_create(
    task = task,
    title = "Gather information",
    description = "Find necessary information for the presentation",
    status = "new",
    deadline = timezone.now() + timedelta(days=2),
)

subtask2, created = SubTask.objects.get_or_create(
    task = task,
    title = "Create slides",
    description = "Create presentation slides",
    status = "new",
    deadline = timezone.now() + timedelta(days=1),
)

new_tasks = Task.objects.filter(status="new")

print(list(new_tasks))

exp_subtasks = SubTask.objects.filter(status="done", deadline__lt=timezone.now())

print(list(exp_subtasks))

######################################################################################
print("update")
task_update = Task.objects.get(
title = "Prepare presentation",
)
task_update.status = "In_progress"
task_update.save()

print("updated status:", task_update.status)

subtask1_update = SubTask.objects.get(
title = "Gather information",
)
old_deadline = subtask1_update.deadline
subtask1_update.deadline = old_deadline - timedelta(days=2)
subtask1_update.save()
print("updated deadline:", subtask1_update.deadline)

subtask2_update = SubTask.objects.get(
title = "Create slides",
)
subtask2_update.description = "Create and format presentation slides"
subtask2_update.save()
print("updated description:", subtask2_update.description)
###################################################################################
print("Delete")
task_dell=Task.objects.get(
    title = "Prepare presentation"
)
print("deleted task:", task_dell)
task_dell.delete()