from rest_framework.views import APIView
from .utils import CeleryBeatTask
from rest_framework.response import Response
from django_celery_beat.models import PeriodicTask
from .serializers import IntervalSerializer,CrontabSerializer
from .cusresponse import JsResponse

# Create your views here.

class CreatPT(APIView):

    def post(self,request):
        # interval:int = request.data.get('interval')
        # name:str = request.data.get('name')
        # task: str = request.data.get('task', 'periodtask.tasks.run_shell')
        # pyname:str = request.data.get('pyname')
        # if CeleryBeatTask.name_exist(name):
        #     return Response(data={'msg': f'create fail {name}已经存在 or 不能为空'})
        serializer = IntervalSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            pt = serializer.save()
            return Response(data={'id':pt.id}, status=201)
        else:
            return JsResponse(data = serializer.errors, code=False,msg=serializer.error_messages)


class CreatCrontab(APIView):

    def post(self,request):
        # name:str = request.data.get('name')
        # minute=request.data.get('minute')
        # hour=request.data.get('hour')
        # task:str=request.data.get('task','periodtask.tasks.run_shell')
        # pyname: str = request.data.get('pyname')
        # if CeleryBeatTask.name_exist(name):
        #     return Response(data={'msg': f'create fail {name}已经存在 or 不能为空'})
        # pt = CeleryBeatTask.create_crontab(name=name,minute=minute,hour=hour,task=task,pyname=pyname)
        #
        # return Response(data={'msg':'success','id':pt.id})
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
                    int(interval)
                except:
                    return JsResponse(code=False, msg='interval必须是一个整数')
                return JsResponse(code=False, msg='interval不能为空 or ')
            pt.update_interval(interval)

        elif pt.periodic_task.crontab:
            if not minute and not hour:
                return JsResponse(code=False, msg='minute hour不能为空')
            if hour != '*':
                try:
                    int(minute)
                    int(hour)
                except:
                    return JsResponse(code=False, msg='miute hour必须是一个整数')
            pt.update_crontab(minute,hour)

        return JsResponse(msg='update success')







