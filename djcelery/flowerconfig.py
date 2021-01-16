import os
# 设置代理人broker
CELERY_BROKER_URL = os.environ.get('REDIS_TCP_ADDR', "redis://127.0.0.1:6379/5")

#Port
port = 5555

# Enable debug logging
logging = 'INFO'

