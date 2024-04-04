#!/bin/bash
PORT=${PORT:-8000}
WORKERS=${WORKERS:-2}
python3 manage.py migrate
python3 manage.py collectstatic --noinput
# gunicorn --bind 0.0.0.0:$PORT --workers=$WORKERS virtumall.wsgi:application
gunicorn --bind 0.0.0.0:$PORT --workers=$WORKERS --threads=5 virtumall.wsgi:application
