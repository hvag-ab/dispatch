from django.urls import path

from .views import CreatPT,StopPT,UpdatePT,StartPT,DeletePT,CreatCrontab

app_name = "pt"

urlpatterns = [
    path("create", CreatPT.as_view()),
    path("create_cron", CreatCrontab.as_view()),
    path("delete", DeletePT.as_view()),
    path("stop", StopPT.as_view()),
    path("update", UpdatePT.as_view()),
    path("start", StartPT.as_view()),

]