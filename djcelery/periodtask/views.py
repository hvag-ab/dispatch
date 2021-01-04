from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .utils import CeleryBeatTask
from rest_framework.response import Response
from django_celery_beat.models import PeriodicTask
from .serializers import IntervalSerializer,CrontabSerializer,PeriodTaskSerializer,JobSerializer
from .cusresponse import JsResponse
from .models import Job

# Create your views here.

class CreatPT(APIView):

    def post(self,request):
        serializer = IntervalSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            pt = serializer.save()
            return Response(data={'id':pt.id}, status=201)
        else:
            return JsResponse(data = serializer.errors, code=False,msg=serializer.error_messages)


class CreatCrontab(APIView):

    def post(self,request):
        serializer = CrontabSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            pt = serializer.save()
            return Response(data={'id': pt.id}, status=201)
        else:
            return JsResponse(data=serializer.errors, code=False, msg=serializer.error_messages)



class StopPT(APIView):
    def post(self, request):
        id = request.data.get("id")
        pt = PeriodicTask.objects.get(id=id)
        pt = CeleryBeatTask(pt)
        pt.stoptask()
        return JsResponse(msg='pause success')


class StartPT(APIView):
    def post(self, request):
        id = request.data.get("id")
        pt = PeriodicTask.objects.get(id=id)
        pt = CeleryBeatTask(pt)
        pt.starttask()

        return JsResponse(msg='starte success')


class DeletePT(APIView):
    def post(self, request):
        id = request.data.get("id")
        pt = PeriodicTask.objects.get(id=id)
        pt = CeleryBeatTask(pt)
        bol = pt.deltask()
        if bol:
            return JsResponse(msg='delete success')
        else:
            return JsResponse(code=False,msg='the task must be pause status')



class UpdatePT(APIView):
    def post(self, request):
        id = request.data.get("id")
        interval = request.data.get('interval')
        minute = request.data.get('minute')
        hour = request.data.get('hour')

        pt = PeriodicTask.objects.get(id=id)
        pt = CeleryBeatTask(pt)

        if pt.periodic_task.interval:
            if not interval or interval.isdigit():
                try:
                    it = int(interval) > 0
                    if not it:
                        raise
                except:
                    return JsResponse(code=False, msg='interval必须是一个正整数')
                return JsResponse(code=False, msg='interval不能为空')
            pt.update_interval(interval)

        elif pt.periodic_task.crontab:
            if not minute and not hour:
                return JsResponse(code=False, msg='minute hour不能为空')
            if hour != '*':
                try:
                    mn = int(minute) > 0 or int(minute)<60
                    h = int(hour) > 0 or int(hour)<24
                    if not mn or not h:
                        return JsResponse(code=False, msg='hour必须在1-23 minute必须在1-59')
                except:
                    return JsResponse(code=False, msg='miute hour必须是一个整数')
            pt.update_crontab(minute,hour)

        return JsResponse(msg='update success')


class QueryTask(ListAPIView):
    queryset = PeriodicTask.objects.select_related().exclude(name = 'celery.backend_cleanup')
    serializer_class = PeriodTaskSerializer








