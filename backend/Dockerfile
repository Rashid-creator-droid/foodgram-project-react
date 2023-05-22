FROM python:3.11-slim

RUN mkdir /app
WORKDIR /app
COPY ./foodgram .
COPY entrypoint.sh .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
