#!/bin/bash
PORT=${PORT:-8000}
WORDERS=${WORDERS:-2}
python3 manage.py migrate
gunicorn --bind 0.0.0.0:$PORT --workers=$WORKERS virtumall.wsgi:application
