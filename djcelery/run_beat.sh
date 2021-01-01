#!/bin/sh

# wait for mysql
# server to start

sleep 10
# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
python -m celery -A core.celery beat --loglevel INFO