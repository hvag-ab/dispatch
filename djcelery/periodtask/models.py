from django.db import models
from django_celery_beat.models import PeriodicTask
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Job(models.Model):
    """Class describing a computational job"""

    # list of statuses that job can have
    STATUSES = (
        ('waiting', 'waiting'),
        ('pending', 'pending'),
        ('finished', 'finished'),
        ('failed', 'failed'),
    )
    periodtask = models.OneToOneField(PeriodicTask,on_delete=models.CASCADE,default=None)
    status = models.CharField(choices=STATUSES, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    result = models.TextField(null=True)



@receiver(post_save, sender=PeriodicTask)
def create_job(sender, instance, created, **kwargs):
    if created:
        Job.objects.create(periodtask=instance, status='waiting')
