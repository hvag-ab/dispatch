import os
from django.utils import timezone
from celery import Celery
from celery import platforms

# 为celery设置环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
# 创建celery app
app = Celery("core")
# Using a string here means the worker will not have to
# pickle the object when using Windows.
# 从单独的配置模块中加载配置
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()#为了重用 Django APP，通常是在单独的 tasks.py 模块中定义所有任务。Celery 会自动发现这些模块：
# 解决时区问题,定时任务启动就循环输出
# app.now = timezone.now
# 强制以root用户运行 django 运行用户实际为非root用户
platforms.C_FORCE_ROOT = True

@app.task(bind=True)
def debug_task(self):
  print('Request: {0!r}'.format(self.request)) #dumps its own request information


"""
celery并发计算规则
celery任务并发只与celery配置项CELERYD_CONCURRENCY 有关，与CELERYD_MAX_TASKS_PER_CHILD没有关系，即CELERYD_CONCURRENCY=2，只能并发2个worker，
此时任务处理较大的文件时，执行两次可以看到两个task任务并行执行，而执行第三个任务时，开始排队，直到两个worker执行完毕。
"""