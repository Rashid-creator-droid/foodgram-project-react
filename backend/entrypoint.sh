#! /bin/bash

python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input
python3 manage.py loaddata data/ingredients.json
gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000