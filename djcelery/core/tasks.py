from celery import shared_task
import random
import os
from django.conf import settings

@shared_task
def sample_task():
    print(f"The sample task just ran.{random.random()}")







