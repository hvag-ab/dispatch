from django.http import JsonResponse
from django.views import View
from orders import tasks
import logging
import time

js = logging.getLogger('js')
tf = logging.getLogger('tf')
stash = logging.getLogger('logstash')


class TestCelery(View):

    def get(self, request, *args, **kwargs):
        h2 = tasks.sub.delay(23, 100)

        js.error('test eror')
        tf.error('test eror')
        stash.error('test eror')

        # print(h2)
        # print(h2.wait()) 获取返回值 但是这是要等着celery执行完后 就不存在异步效果
        # h2 = tasks.sub.apply_async(queue='low_priorityy', args=(10, 50))
        # h2 = tasks.sub.apply_async(queue='high_priority', kwargs={'a': 10, 'b': 5})
        task_id = h2.task_id
        return JsonResponse(data={'task_id': task_id}, status=200)

class Te(View):

    def get(self, request, *args, **kwargs):

        js.error(f'test eror-{time.time()}')
        tf.error('test eror')
        stash.error('test eror')
        return JsonResponse(data={'task_id': 2}, status=200)



"""
from celery.result import AsyncResult
res=AsyncResult("62051878-ca77-4895-a61f-6f9525681347") # 参数为task id
result = res.result # 通过task_id 获取 异步执行返回结果
res.status 表示 运行状态
res.traceback 表示运行的异常错误



cd 进入manage.py同级目录
$ pip install -r requirements.txt
$ ./manage.py makemigrations
$ ./manage.py migrate
$ python3 -m celery -A core.celery worker --loglevel INFO (-P eventlet windows下使用) 
$ python3 -m celery -A core.celery beat --loglevel INFO  # You need to run on other terminal.
$ ./manage.py shell
$ python3 -m celery purge -Q [queue_name] 清空队列
"""

##########

"""
celery+supervisor启动works和beat
只需要修改celery.ini配置文件里面的执行命令即可

配置celery.ini
root@StarMeow-Svr:~/django-web# cd Supervisor/
(Supervisor) root@StarMeow-Svr:~/django-web/Supervisor# ls
celery.ini  supervisord.conf
(Supervisor) root@StarMeow-Svr:~/django-web/Supervisor# vim celery.ini
celery.ini

# 配置内容 
[program:celery] 
# celery命令的绝对路径 
command=/root/.pyenv/versions/StarMeow/bin/celery -A StarMeow worker -B -l info 
# 项目路径 
directory=/root/django-web/StarMeow 
# 日志文件路径 
stdout_logfile=/var/log/myweb/celery.log 
# 自动重启 
autorestart=true 
# 如果设置为true,进程则会把标准错误输出到supervisord后台的标准输出文件描述符 
redirect_stderr=true 
重载
因为之前配置了自动重载脚本，只需要执行下即可

(Supervisor) root@StarMeow-Svr:~/django-web/Supervisor# cd ..
root@StarMeow-Svr:~/django-web# ./SvReload.sh 
正在更新Supervisor配置···
Restarted supervisord

查看celery日志
root@StarMeow-Svr:~/django-web# cat /var/log/myweb/celery.log


# 守护进程
celery multi start w1 -A celery_tasks.main -l info --logfile=./celerylog.log
# 停止和重启 分别将 start 改为 stop / restart
守护进程的另一种方式，使用supervisor，这是一个管理进程的工具，这种启动方式就是用supervisor接管celery


pip install django-celery-results  这是保存celery执行后的结果
2.配置settings.py，注册app

INSTALLED_APPS = (
    ...,
    'django_celery_results',
)
4.修改backend配置，将redis改为django-db

#CELERY_RESULT_BACKEND = 'redis://10.1.210.69:6379/0' # BACKEND配置，这里使用redis

CELERY_RESULT_BACKEND = 'django-db'  #使用django orm 作为结果存储
5.修改数据库

python3 manage.py migrate django_celery_results



pply_async可以使用并发，这是其强大之处

# -c参数：表示worker创建的并发线程数 启动多个队列
(venv) $ celery -A proj worker -l info -Q default -c 2
(venv) $ celery -A proj worker -l info -Q low_priority -c 1
(venv) $ celery -A proj worker -l info -Q high_priority -c 4
指定并发池的上下限

​
(venv) $ celery -A proj worker -l info -Q default --autoscale 4,2
(venv) $ celery -A proj worker -l info -Q low_priority --autoscale 2,1
(venv) $ celery -A proj worker -l info -Q high_priority --autoscale 8,4
保持并发数接近CPU核心数量。如果服务器有4个核心CPU，则最大并发数应该是4,更大的数字可工作但效率会下降

任务可以在很多单独的任务队列中执行，但将所有内容放在单个队列中会更好.

在单个队列中避免FIFO，需对每个任务定义优先级，整数范围为0-9。
add.apply_async(queue='high_priority', priority=0, kwargs={'a': 10, 'b': 5})
add.apply_async(queue='high_priority', priority=5, kwargs={'a': 10, 'b': 5})
add.apply_async(queue='high_priority', priority=9, kwargs={'a': 10, 'b': 5})

不同app task指定不同的队列
CELERY_QUEUES = (
Queue("default",Exchange("default"),routing_key="default"),
Queue("for_task_A",Exchange("for_task_A"),routing_key="for_task_A"),
Queue("for_task_B",Exchange("for_task_B"),routing_key="for_task_B") 
)

CELERY_ROUTES = {
'tasks.taskA':{"queue":"for_task_A","routing_key":"for_task_A"},
'tasks.taskB':{"queue":"for_task_B","routing_key":"for_task_B"}
}
3.启动worker来指定task

celery -A tasks worker -l info -n workerA.%h -Q for_task_A


、time_limit和soft_time_limit区别

time_limit : 执行超时，结束signal 9 (SIGKILL) 执行的子进程，状态："status": "FAILURE" 超过直接杀死当前执行任务的worker 日志会抛出一个错误
soft_time_limit ：执行超时，用一个异常SoftTimeLimitExceeded来捕捉，状态："status": "SUCCESS"
目前只能在linux操作系统才有效

handler_upload_data.apply_async((full_path,), soft_time_limit=10)
handler_upload_data.apply_async((full_path,), time_limit=10)

celery指定任务执行时间
import datetime
 
 
def in_run_time(start, end):

    用来给任务判断，在不在可执行的时间里，是不是需要丢到定时里
    Args:
        start: 任务开始执行的时间，格式如 "00:00:00"
        end:  任务停止执行的时间，格式如 "07:00:00"
    Returns:
  
    current_date = str(datetime.datetime.now().date()) + " "
    start_time = datetime.datetime.strptime(current_date + start, '%Y-%m-%d %H:%M:%S')
    end_time = datetime.datetime.strptime(current_date + end, '%Y-%m-%d %H:%M:%S')
    current_date = datetime.datetime.now()
    if (start_time < current_date) and (current_date < end_time):
        return True
    else:
        return False
 
 
def get_nextday_run_time(start, end):
   
    根据当前时间，和起止时间，得出该任务应该执行的时间。
    Args:
        start: 任务开始执行的时间，格式如 "00:00:00"
        end:  任务停止执行的时间，格式如 "07:00:00"
    Returns:
  
    current_date = datetime.datetime.now().date()
    end_time = datetime.datetime.strptime(str(current_date) + " " + end, '%Y-%m-%d %H:%M:%S')
    current_time = datetime.datetime.now()
    # 如果现在还没到今天的执行时间，那么任务放到今天的执行时间来执行
    if current_time > end_time:
        current_date += datetime.timedelta(days=1)
    run_time_str = str(current_date) + " " + start
    # 执行-北京时间
    run_time = datetime.datetime.strptime(run_time_str, '%Y-%m-%d %H:%M:%S')
    run_time = run_time + datetime.timedelta(hours=-8)
    return run_time
 
 
def get_run_time_by_bj_time(bj_time):
    
    将时间格式字符串转换为datetime格式
    Args:
        bj_time: 指定执行时间 type-str 如 "2019-08-21 13:21:00"
    Returns:
  
    run_time = datetime.datetime.strptime(bj_time, '%Y-%m-%d %H:%M:%S')
    run_time = run_time + datetime.timedelta(hours=-8)
    return run_time
    
start = "00:00:00"
end = "07:00:00"
work.apply_async(args=[scan_data], eta=get_nextday_run_time(start, end), 
                 queue="队列名，没有可删除参数", routing_key="队列key，没有可删除参数")

"""
