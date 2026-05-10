from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from my_new_app.models import Task


@receiver(pre_save, sender=Task)
def remember_old_status(sender, instance, **kwargs):

    if not instance.pk:
        instance._old_status = None
        return

    try:
        old_task = Task.objects.get(pk=instance.pk)
        instance._old_status = old_task.status
    except Task.DoesNotExist:
        instance._old_status = None


@receiver(post_save, sender=Task)
def notify_about_status_change(sender, instance, created, **kwargs):

    if created:
        return

    old_status = getattr(instance, '_old_status', None)

    if old_status == instance.status:
        return

    print(f'OLD STATUS: {old_status}')
    print(f'NEW STATUS: {instance.status}')

    owner = getattr(instance, 'owner', None)

    print(owner)

    # временно без email
    send_mail(
        subject='Task status updated',
        message=f'Status changed: {old_status} -> {instance.status}',
        from_email='megaspektr.e@gmail.com',
        recipient_list=['lyt.kateryna@gmail.com']

    )