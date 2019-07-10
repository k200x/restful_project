import gevent.monkey
gevent.monkey.patch_all()

import multiprocessing

debug = False
loglevel = 'INFO'
bind = '0.0.0.0:9112'
pidfile = '/var/www/log/xkool_log/gunicorn_log/gunicorn.pid'
logfile = '/var/www/log/xkool_log/gunicorn_log/debug.log'
errorlog = "/var/www/log/xkool_log/gunicorn_log/error.log"
accesslog = "/var/www/log/xkool_log/gunicorn_log/access.log"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
capture_output = "/var/www/log/user_log/gunicorn_log/access.log"
capture_output = True
keepalive = 5

workers = multiprocessing.cpu_count() * 2 + 1

worker_class = 'gunicorn.workers.ggevent.GeventWorker'

x_forwarded_for_header = 'X-FORWARDED-FOR'

