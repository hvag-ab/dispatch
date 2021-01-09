import os
# 设置代理人broker
CELERY_BROKER_URL = os.environ.get('REDIS_TCP_ADDR', "redis://127.0.0.1:6379/5")
# 指定 结果Backend
CELERY_RESULT_BACKEND = os.environ.get('REDIS_TCP_ADDR', "redis://127.0.0.1:6379/6")
# BROKER_POOL_LIMIT = 50
# CELERY_REDIS_MAX_CONNECTIONS = 60
# BROKER_TRANSPORT_OPTIONS = {
#     "max_connections": 400,
# }

# 指定时区，默认是 UTC
CELERY_TIMEZONE='Asia/Shanghai'

imports = ('tasks',)
# 初始化定时任务
# CELERY_BEAT_SCHEDULE = {
#     "sample_task": {
#         "task": "core.tasks.sample_task",
#         "schedule": crontab(minute="*/1"),
#     },
# }
# celery 序列化与反序列化配置
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle', 'json']


# celery任务执行结果的超时时间，
CELERY_TASK_RESULT_EXPIRES = 10
# 设置默认不存结果
CELERY_IGNORE_RESULT = True

# celery 的启动工作数量设置
CELERY_WORKER_CONCURRENCY = 10

# 有些情况可以防止死锁
CELERY_FORCE_EXECV = True

# 任务预取功能，会尽量多拿 n 个，以保证获取的通讯成本可以压缩。
CELERYD_PREFETCH_MULTIPLIER = 20

# 设置并发的worker数量
CELERYD_CONCURRENCY = 4

# celery 的 worker 执行多少个任务后进行重启操作
CELERY_WORKER_MAX_TASKS_PER_CHILD = 100

# 任务发送完成是否需要确认，这一项对性能有一点影响
CELERY_ACKS_LATE = False

# 每个worker执行了多少任务就会销毁，防止内存泄露，默认是无限的
CELERYD_MAX_TASKS_PER_CHILD = 4

# 禁用所有速度限制，如果网络资源有限，不建议开足马力。
CELERY_DISABLE_RATE_LIMITS = True

# 规定完成任务的时间
CELERYD_TASK_TIME_LIMIT = 15 * 60  # 在15分钟内完成任务，否则执行该任务的worker将被杀死，任务移交给父进程

# 设置默认的队列名称，如果一个消息不符合其他的队列就会放在默认队列里面，如果什么都不设置的话，数据都会发送到默认的队列中
CELERY_DEFAULT_QUEUE = "default"

# 设置详细的队列
CELERY_QUEUES = {
    "default": { # 这是上面指定的默认队列
        "exchange": "default",
        "exchange_type": "direct",
        "routing_key": "default"
    },
    "beat_queue": {
        "exchange": "beat_queue",
        "exchange_type": "direct",
        "routing_key": "beat_queue"
    }

}

# celery beat配置（周期性任务设置）
# CELERY_ENABLE_UTC = False
# DJANGO_CELERY_BEAT_TZ_AWARE = False
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 把要发送的邮件显示再控制台上，方便调试
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.qq.com'  # 如果是 163 改成 smtp.163.com
EMAIL_PORT = 465
EMAIL_HOST_USER = 'qq邮箱'  # 帐号
EMAIL_HOST_PASSWORD = 'qq授权码'  # 授权码
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
ADMINS = [("testuser", "test.user@qq.com"), ]

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'periodtask.custom_exception.exception_handler',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}