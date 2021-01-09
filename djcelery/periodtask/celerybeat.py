import pytz, json

from django_celery_beat import models as celery_models


def task_add(task_name, task_class, task_cron, task_kwargs=None, task_queue=None, one_off=False):
    '''
    任务添加
    :param task_name: 任务名称
    :param task_queue: 任务队列
    :param task_kwargs: 任务传递参数
    :param task_class: 任务执行类
    :param task_cron: 任务定时的表达式
    :param one_off: 是否只运行一次 默认false
    :return:
    '''
    # 获取crontab,没有就创建
    schedule, _ = celery_models.CrontabSchedule.objects.get_or_create(**task_cron,
                                                                      timezone=pytz.timezone('Asia/Shanghai'))

    task = celery_models.PeriodicTask.objects.create(crontab=schedule, name=task_name, task=task_class)
    task.queue = task_queue
    task.exchange = task_queue
    task.routing_key = task_queue
    if task_kwargs:
        task_kwargs.update({'name':task_name})
    task.kwargs = json.dumps(task_kwargs)
    task.enabled = True
    task.one_off = one_off
    task.save()
    celery_models.PeriodicTasks.changed(task)
    return task.id


def task_update(task_id, task_name=None, task_queue=None, task_cron=None, enabled=None):
    '''
    修改任务
    :param task_id: 需要修改的任务的id
    :param task_name: 修改后的任务名称，若需要修改，以字符串形式传递
    :param task_queue: 修改后的任务队列名称，若需要修改，以字符串形式传递
    :param task_cron: 修改后的时间表
    :return:
    '''
    per_task = celery_models.PeriodicTask.objects.get(id=task_id)
    if task_name and task_name != per_task.name:
        per_task.name = task_name
    if task_queue and task_queue != per_task.queue:
        per_task.queue = task_queue
        per_task.exchange = task_queue
        per_task.routing_key = task_queue
    if enabled is not None and enabled != per_task.enabled:
        per_task.enabled = enabled
    if task_cron:
        schedule,_ = celery_models.CrontabSchedule.objects.get_or_create(**task_cron, timezone=pytz.timezone('Asia/Shanghai'))
        per_task.crontab = schedule
    per_task.save()
    celery_models.PeriodicTasks.changed(per_task)
    return per_task.name, per_task.queue, per_task.args, per_task.task, per_task.crontab


def task_del(task_id):
    '''
    删除任务
    :param task_id: 任务id
    :return:
    '''
    # 暂停执行周期性任务
    task_query = celery_models.PeriodicTask.objects.get(id=task_id)
    task_query.enabled = False
    task_query.save()
    # 删除任务
    rows,_ = task_query.delete()

    celery_models.PeriodicTasks.update_changed()
    return rows


def task_list(task_name, task_queue):
    '''
    任务查询
    :param task_name: 任务名称
    :param task_queue: 任务队列
    :return: task_name任务名称、task_queue任务队列、task_args任务参数、task_class任务执行类、task_cron任务定时的表达式
    '''
    # 查询目前满足条件的所有周期性任务
    per_task = celery_models.PeriodicTask.objects.get(name=task_name, queue=task_queue)
    data = {
        "task_name": per_task.name,
        "task_queue": per_task.queue,
        "task_kwargs": per_task.kwargs,
        "task_class": per_task.task,
        "task_cron": per_task.crontab,
    }
    return data


def queue_update(queue_name_pre, queue_name_cur):
    '''
    更改任务的队列
    :param queue_name_pre: 要改的队列名称
    :param queue_name_cur: 改变后的队列名
    :return:
    '''
    all_tasks = celery_models.PeriodicTask.objects.filter(queue=queue_name_pre)
    all_tasks_ids = [per_task.id for per_task in all_tasks]
    for task_id in all_tasks_ids:
        task_query = celery_models.PeriodicTask.objects.get(id=task_id)
        task_query.queue = queue_name_cur
        task_query.exchange = queue_name_cur
        task_query.routing_key = queue_name_cur
        task_query.save()
    celery_models.PeriodicTasks.update_changed()
    all_tasks = celery_models.PeriodicTask.objects.filter(queue=queue_name_cur)
    return all_tasks