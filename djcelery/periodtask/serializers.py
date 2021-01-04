from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django_celery_beat.models import PeriodicTask,IntervalSchedule,CrontabSchedule
from .utils import CeleryBeatTask
from .models import Job


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
    minute = serializers.IntegerField(min_value=1,max_value=59)
    hour = serializers.CharField(default="*")

    def validate_hour(self, hour):

        if hour == "*":
            return hour
        try:
            h = int(hour)
            if h <= 0 or h>= 24:
                raise serializers.ValidationError("hour必须在0到24之间")
        except:
            raise serializers.ValidationError("hour必须在0到24之间 or *")
        return hour

    def save(self):  # save并不一定是用来create或者 update 可以用来实现自己的逻辑
        minute = self.validated_data['minute']
        hour = self.validated_data['hour']
        name = self.validated_data['name']
        pyname = self.validated_data['pyname']
        task = self.validated_data['task']
        pt = CeleryBeatTask.create_crontab(name=name,minute=minute,hour=hour,task=task,pyname=pyname)
        return pt


class CrontabTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrontabSchedule
        exclude = ('timezone','id')


class IntervalTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntervalSchedule
        exclude = ('id',)


class JobSerializer(serializers.ModelSerializer):
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = Job
        fields = ['status','result','updated_at']


class PeriodTaskSerializer(serializers.ModelSerializer):

    crontab = CrontabTaskSerializer()
    interval = IntervalTaskSerializer()
    job = JobSerializer()


    class Meta:
        model = PeriodicTask
        fields = "__all__"

