from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django_celery_beat.models import PeriodicTask
from .serializers import CrontabSerializer,PeriodTaskSerializer,JobSerializer
from .cusresponse import JsResponse
from .celerybeat import task_add,task_update,task_del

# Create your views here.


class CreatCrontab(APIView):

    def post(self,request):

        serializer = CrontabSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task_id = serializer.save()
        return JsResponse(data={'id': task_id})



class StopPT(APIView):
    def post(self, request):
        id = request.data.get("id")
        try:
            task_update(id,enabled=False)
            return JsResponse(msg='pause success')
        except Exception as e:
            return JsResponse(msg=str(e),code=False)


class StartPT(APIView):
    def post(self, request):
        id = request.data.get("id")
        try:
            task_update(id,enabled=True)
            return JsResponse(msg='starte success')
        except Exception as e:
            return JsResponse(msg=str(e), code=False)


class DeletePT(APIView):
    def post(self, request):
        id = request.data.get("id")
        try:
            rows = task_del(id)

            if rows>0:
                return JsResponse(msg='delete success')
            else:
                return JsResponse(code=False,msg='delete fail')
        except Exception as e:
            return JsResponse(msg=str(e), code=False)



class UpdatePT(APIView):
    def post(self, request):
        id = request.data.get("id")
        minute = request.data.get('minute')
        hour = request.data.get('hour')
        try:
            task_update(id, task_cron={'minute': minute, 'hour': hour})
            return JsResponse(msg='update success')
        except Exception as e:
            return JsResponse(msg=str(e), code=False)


class QueryTask(ListAPIView):
    queryset = PeriodicTask.objects.select_related().exclude(name = 'celery.backend_cleanup')
    serializer_class = PeriodTaskSerializer








