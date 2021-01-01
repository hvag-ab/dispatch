import os
from django.utils import timezone
from celery import Celery

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
app.now = timezone.now

@app.task(bind=True)
def debug_task(self):
  print('Request: {0!r}'.format(self.request)) #dumps its own request information