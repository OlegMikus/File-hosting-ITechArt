#!/bin/bash

python manage.py makemigrations

python manage.py migrate

exec gunicorn src.config.wsgi:application --bind 0.0.0.0:8000 --reload --workers=3 --timeout=120