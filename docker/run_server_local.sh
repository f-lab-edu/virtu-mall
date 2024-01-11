#!/bin/bash
PORT=${PORT:-8000}
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver settings --virtumall.settings.development
