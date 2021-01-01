import json
import pytz
from functools import wraps

from django_celery_beat.models import PeriodicTask,IntervalSchedule,CrontabSchedule
from .models import Job

"""
#基于Crontab 创建 
schedule, _ = CrontabSchedule.objects.get_or_create(
   minute='30',
   hour='*',
   day_of_week='*',
   day_of_month='*',
   month_of_year='*',
   timezone=pytz.timezone('Asia/Shanghai')
)
"""

class CeleryBeatTask:

    def __init__(self, pt:PeriodicTask):
        # pt是PeriodicTask的实例相当于这个模型的一条记录 通过model.objects.get_or_create()
        self.periodic_task = pt

    @classmethod
    def name_exist(cls,name):

        if not name:
            return True
        bol = PeriodicTask.objects.filter(name=name).exists()
        return bol

    @classmethod
    def create_interval(cls,interval:int, name:str, task:str='app名.tasks.任务函数名', expires=None, *arg,**kwargs):
        # interval int 每隔多少秒
        """
        IntervalSchedule.DAYS 固定间隔天数
        IntervalSchedule.HOURS 固定间隔小时数
        IntervalSchedule.MINUTES 固定间隔分钟数
        IntervalSchedule.SECONDS 固定间隔秒数
        IntervalSchedule.MICROSECONDS 固定间隔微秒
        """

        schedule, created = IntervalSchedule.objects.get_or_create(
            every=interval,
            period=IntervalSchedule.SECONDS,
        )
        dic = dict(
            enabled=True,
            interval=schedule,  # we created this above.
            name=name,  # simply describes this periodic task.
            task=task,  # name of task.
        )
        if arg:
            arg = json.dumps(arg)
            dic['args'] = arg
        if kwargs:
            kwargs = json.dumps(kwargs)
            dic['kwargs'] = kwargs
        print(dic)
        pt = PeriodicTask.objects.create(**dic)
        return cls(pt)

    @classmethod
    def create_crontab(cls, name:str,minute="30",hour="*",day_of_week="*",day_of_month='*', task:str='app名.tasks.任务函数名', expires=None, *arg,**kwargs):
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=minute,
            hour=hour,
            day_of_week=day_of_week,
            day_of_month=day_of_month,
            month_of_year='*',
            timezone=pytz.timezone('Asia/Shanghai')
        )
        dic = dict(
            enabled=True,
            crontab=schedule,  # we created this above.
            name=name,  # simply describes this periodic task.
            task=task,  # name of task.
        )
        if arg:
            arg = json.dumps(arg)
            dic['args'] = arg
        if kwargs:
            kwargs = json.dumps(kwargs)
            dic['kwargs'] = kwargs
        pt = PeriodicTask.objects.create(**dic)
        return cls(pt)

    @property
    def id(self):
        return self.periodic_task.id

    def starttask(self):
        """
        启动任务
        """
        self.periodic_task.enabled = True
        self.periodic_task.save()

    def stoptask(self):
        """
        停止任务
        """
        self.periodic_task.enabled = False
        self.periodic_task.last_run_at = None
        self.periodic_task.save()

    def deltask(self):
        """
        删除任务
        """
        self.periodic_task.delete()

    def update_interval(self,interval:int):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=interval,
            period=IntervalSchedule.SECONDS,
        )
        self.periodic_task.interval=schedule
        self.periodic_task.last_run_at = None
        self.periodic_task.save()

    def update_crontab(self, minute:str,hour:str,day_of_week="*",day_of_month='*'):
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=minute,
            hour=hour,
            day_of_week=day_of_week,
            day_of_month=day_of_month,
            month_of_year='*',
            timezone=pytz.timezone('Asia/Shanghai')
        )
        self.periodic_task.crontab=schedule
        self.periodic_task.last_run_at = None
        self.periodic_task.save()


def update_job(fn):

    @wraps(fn)
    def wrapper(**kwargs):
        pyname = kwargs.get('pyname')
        jobs = Job.objects.filter(func_name=pyname)
        if not jobs:
            Job.objects.create(func_name=pyname,task_name=fn.__name__,argument=str(kwargs))
        else:
            job = jobs[0]
            if job.status == 'pending':
                pass
            else:
                jobs.update(status = 'pending')
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

