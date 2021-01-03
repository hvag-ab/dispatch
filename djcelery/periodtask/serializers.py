from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
import re
from django_celery_beat.models import PeriodicTask,IntervalSchedule,CrontabSchedule
from .utils import CeleryBeatTask


class TaskSerializer(serializers.Serializer):

    name = serializers.CharField(
        max_length=255,
        min_length=1,
        validators=[UniqueValidator(queryset=PeriodicTask.objects.all())])
    task = serializers.CharField(default='periodtask.tasks.run_shell')
    pyname = serializers.CharField(required=True)


class IntervalSerializer(TaskSerializer):
    interval = serializers.IntegerField(min_value=5)

    def save(self):

        interval = self.validated_data['interval']
        name = self.validated_data['name']
        pyname = self.validated_data['pyname']
        task = self.validated_data['task']
        pt = CeleryBeatTask.create_interval(interval, name, task, pyname=pyname)
        return pt


class CrontabSerializer(TaskSerializer):
    minute = serializers.IntegerField(min_value=1)
    hour = serializers.CharField(default="*")

    def validate_hour(self, hour):

        if hour == "*":
            return hour
        try:
            int(hour)
        except:
            raise serializers.ValidationError("hour 必须是一个整数or *")
        return hour

    def save(self):  # save并不一定是用来create或者 update 可以用来实现自己的逻辑
        minute = self.validated_data['minute']
        hour = self.validated_data['hour']
        name = self.validated_data['name']
        pyname = self.validated_data['pyname']
        task = self.validated_data['task']
        pt = CeleryBeatTask.create_crontab(name=name,minute=minute,hour=hour,task=task,pyname=pyname)
        return pt
