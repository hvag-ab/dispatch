from django.db import models

# Create your models here.

class Job(models.Model):
    """Class describing a computational job"""

    # list of statuses that job can have
    STATUSES = (
        ('pending', 'pending'),
        ('finished', 'finished'),
        ('failed', 'failed'),
    )

    task_name = models.CharField(max_length=20)
    func_name = models.CharField(max_length=20)
    status = models.CharField(choices=STATUSES, max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    argument = models.CharField(max_length=255)
    result = models.CharField(null=True,max_length=255)

