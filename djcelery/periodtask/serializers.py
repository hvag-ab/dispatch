from rest_framework import serializers
from rest_framework.validators import UniqueValidator,ValidationError
from django_celery_beat.models import PeriodicTask,IntervalSchedule,CrontabSchedule
from .celerybeat import task_add
from .models import Job
from celery.schedules import crontab


class TaskSerializer(serializers.Serializer):

    name = serializers.CharField(
        max_length=255,
        min_length=1,
        validators=[UniqueValidator(queryset=PeriodicTask.objects.all())])
    task = serializers.CharField(default='periodtask.tasks.run_shell')
    pyname = serializers.CharField(required=True)


class CrontabSerializer(TaskSerializer):
    minute = serializers.CharField(default="0")
    hour = serializers.CharField(default="*")
    day_of_week = serializers.CharField(default="*")


    def save(self):
        name = self.validated_data['name']
        pyname = self.validated_data['pyname']
        task = self.validated_data['task']
        minute = self.validated_data['minute']
        hour = self.validated_data['hour']
        day_of_week = self.validated_data['day_of_week']
        try:
            crontab(minute=minute,hour=hour,day_of_week=day_of_week)
        except Exception as e:
            raise ValidationError(detail="crontab表达式格式错误")
        try:
            task_id = task_add(name, task, {'minute': minute, 'hour': hour,'day_of_week':day_of_week},task_kwargs={'pyname':pyname})
            return task_id
        except Exception as e:
            raise ValidationError(detail=str(e))


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

