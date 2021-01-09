from functools import wraps


from django_celery_beat.models import PeriodicTask
from .models import Job



def update_job(fn):

    @wraps(fn)
    def wrapper(**kwargs):
        name = kwargs.get('name')
        periodtask = PeriodicTask.objects.get(name=name)
        job = Job.objects.get(periodtask=periodtask)
        if job.status == 'pending':
            pass
        else:
            job.status = 'pending'
            job.result = None
            job.save()
            try:
                # execute the function fn
                result,status = fn(**kwargs)
                job.result = result
                if status == 0:
                    job.status = 'finished'
                else:
                    job.status = 'failed'
                job.save()
            except:
                job.result = None
                job.status = 'failed'
                job.save()
    return wrapper

