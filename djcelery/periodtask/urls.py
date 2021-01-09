from django.urls import path

from .views import StopPT,UpdatePT,StartPT,DeletePT,CreatCrontab,QueryTask

app_name = "pt"

urlpatterns = [
    path("create_cron", CreatCrontab.as_view()),
    path("delete", DeletePT.as_view()),
    path("stop", StopPT.as_view()),
    path("update", UpdatePT.as_view()),
    path("start", StartPT.as_view()),
    path("tasks", QueryTask.as_view())
]