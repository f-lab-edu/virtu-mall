import os

if not os.path.exists("./log/gunicorn/"):
    os.makedirs("./log/gunicorn/")

bind = "0.0.0.0:8000"
workers = 2
worker_class = "gevent"
worker_connections = 300
statsd_host = "localhost:8125"
proc_name = "virtumall"
dogstatsd_tags = "virtumall"

reload = True
accesslog = "./log/gunicorn/access.log"
errorlog = "./log/gunicorn/error.log"
loglevel = "info"
