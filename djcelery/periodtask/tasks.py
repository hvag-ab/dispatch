from celery import shared_task
import subprocess
from django.conf import settings
from .utils import update_job


@shared_task
@update_job
def run_shell(**kwargs):
    pyname = kwargs.get('pyname')
    bd = settings.BASE_DIR + '/' + 'script'
    status,output = subprocess.getstatusoutput(f'cd {bd} && python {pyname}.py')
    return output,status