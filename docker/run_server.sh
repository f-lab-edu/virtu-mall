#!/bin/bash
PORT=${PORT:-8000}
WORKERS=${WORKERS:-2}
python3 manage.py makemigrations
python3 manage.py migrate
python manage.py collectstatic
gunicorn --bind 0.0.0.0:$PORT --workers=$WORKERS virtumall.wsgi:application
