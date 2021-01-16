#!/bin/sh

# wait for RabbitMQ server to start

# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
export C_FORCE_ROOT="true"
python3 -m celery -A core.celery worker --loglevel INFO