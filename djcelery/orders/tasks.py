from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

#Celery默认会根据模块的导入方式创建任务名称。可能会与第三方软件包发生冲突，因此每个任务明确设置名称。首选使用proj.package.module.function_name设置。
# @app.task(name='core.tasks.sub',auto_retry=[HTTPException], max_retries=3)
@shared_task
def sub(x, y):
    print(x, y)
    return x - y

    
@shared_task
def send_active_email(to_email, username, token):
    """发送激活邮件"""
    # 组织邮件内容
    subject = 'xxxx'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = """
                        <h1>%s, 欢迎</h1>
                        请点击以下链接激活您的账户(7个小时内有效)<br/>
                        <a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>
                    """ % (username, token, token)

    # 发送激活邮件
    # send_mail(subject=邮件标题, message=邮件正文,from_email=发件人, recipient_list=收件人列表)
    send_mail(subject, message, sender, receiver, html_message=html_message)
