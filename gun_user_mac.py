import os
import gevent.monkey
gevent.monkey.patch_all()

import multiprocessing


# 本地开发

debug = False
loglevel = 'INFO'
bind = '0.0.0.0:9112'
pidfile = '/Users/zhanglei/Desktop/project/majiang/log/user_log/gunicorn_log/gunicorn.pid'
logfile = '/Users/zhanglei/Desktop/project/majiang/log/user_log/gunicorn_log/debug.log'
errorlog = "/Users/zhanglei/Desktop/project/majiang/log/user_log/gunicorn_log/error.log"
accesslog = "/Users/zhanglei/Desktop/project/majiang/log/user_log/gunicorn_log/access.log"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
capture_output = "/Users/zhanglei/Desktop/project/majiang/log/user_log/gunicorn_log/access.log"
capture_output = True
keepalive = 5


#启动的进程数
workers = multiprocessing.cpu_count() * 2 + 1
#workers = 1
worker_class = 'gunicorn.workers.ggevent.GeventWorker'

x_forwarded_for_header = 'X-FORWARDED-FOR'

