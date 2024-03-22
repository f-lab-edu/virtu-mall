import os
from datetime import datetime

if not os.path.exists("./log/gunicorn/"):
    os.makedirs("./log/gunicorn/")

bind = "0.0.0.0:8000"
workers = 2
worker_class = "gevent"
worker_connections = 1000
statsd_host = "localhost:8125"
proc_name = "virtumall"
dogstatsd_tags = "virtumall"

reload = True
accesslog = f"./log/gunicorn/access_{datetime.now().strftime('%Y-%m-%d')}.log"
errorlog = f"./log/gunicorn/error_{datetime.now().strftime('%Y-%m-%d')}.log"
loglevel = "info"
