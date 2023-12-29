#!/bin/bash
PORT=${PORT:-8000}
python3 manage.py migrate
gunicorn --bind 0.0.0.0:$PORT --workers=2 virtumall.wsgi:application
