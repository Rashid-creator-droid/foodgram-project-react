#! /bin/bash

python3 manage.py makemigrations

python3 manage.py migrate --no-input

gunicorn backend.wsgi:application --bind 0.0.0.0:8000