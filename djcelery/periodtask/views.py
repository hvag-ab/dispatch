from django.shortcuts import render
from rest_framework.views import APIView
from .utils import CeleryBeatTask
from rest_framework.response import Response
from django_celery_beat.models import PeriodicTask

# Create your views here.

class CreatPT(APIView):

    def post(self,request):
        interval:int = request.data.get('interval')
        name:str = request.data.get('name')
        task: str = request.data.get('task', 'periodtask.tasks.run_shell')
        pyname:str = request.data.get('pyname')
        if CeleryBeatTask.name_exist(name):
            return Response(data={'msg': f'create fail {name}已经存在 or 不能为空'})
        pt = CeleryBeatTask.create_interval(interval,name,task,pyname=pyname)

        return Response(data={'msg':'success','id':pt.id})

class CreatCrontab(APIView):

    def post(self,request):
        name:str = request.data.get('name')
        minute=request.data.get('minute')
        hour=request.data.get('hour')
        task:str=request.data.get('task','periodtask.tasks.run_shell')
        pyname: str = request.data.get('pyname')
        if CeleryBeatTask.name_exist(name):
            return Response(data={'msg': f'create fail {name}已经存在 or 不能为空'})
        pt = CeleryBeatTask.create_crontab(name=name,minute=minute,hour=hour,task=task,pyname=pyname)

        return Response(data={'msg':'success','id':pt.id})



class StopPT(APIView):
    def post(self, request):
        id = request.data.get("id")
        pt = PeriodicTask.objects.get(id=id)
        pt = CeleryBeatTask(pt)
        pt.stoptask()

        return Response(data={'msg': 'Stopsuccess'})

class StartPT(APIView):
    def post(self, request):
        id = request.data.get("id")
        pt = PeriodicTask.objects.get(id=id)
        pt = CeleryBeatTask(pt)
        pt.starttask()

        return Response(data={'msg': 'started'})

class DeletePT(APIView):
    def post(self, request):
        id = request.data.get("id")
        pt = PeriodicTask.objects.get(id=id)
        pt = CeleryBeatTask(pt)
        pt.deltask()
        return Response(data={'msg': 'delsuccess'})


class UpdatePT(APIView):
    def post(self, request):
        id = request.data.get("id")
        interval: int = request.data.get('interval')
        minute = request.data.get('minute')
        hour = request.data.get('hour')
        print('id',id)
        pt = PeriodicTask.objects.get(id=id)
        pt = CeleryBeatTask(pt)
        if pt.periodic_task.interval:
            if not interval:
                return Response(data={'msg': 'interval不能为空'})
            pt.update_interval(interval)

        elif pt.periodic_task.crontab:
            if not minute and not hour:
                return Response(data={'msg': 'minute hour不能为空'})
            pt.update_crontab(minute,hour)

        else:
            return Response(data={'msg': 'update fail'})
        return Response(data={'msg': 'update sucess'})







