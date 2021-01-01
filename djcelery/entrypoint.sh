#!/usr/bin/env bash
#gunicorn --reload config.wsgi -c ./gunicorn.py -b 0.0.0.0:8888 --log-level=debug
python manage.py makemigrations&&
python manage.py migrate&&
gunicorn -c ./gunicorn.py core.wsgi:application