#!/bin/bash
PORT=${PORT:-8000}
WORKERS=${WORKERS:-2}
python3 manage.py migrate
python3 manage.py collectstatic --noinput
gunicorn virtumall.wsgi:application -c gunicorn.conf.py
# gunicorn --bind 0.0.0.0:$PORT --workers=$WORKERS --threads=10 virtumall.wsgi:application
# gunicorn --bind 0.0.0.0:$PORT --workers=$WORKERS virtumall.wsgi:application
