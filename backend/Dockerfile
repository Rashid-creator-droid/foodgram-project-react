FROM python:3.11-slim

RUN mkdir /app
WORKDIR /app
COPY ./foodgram .
COPY /entrypoint.sh .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
