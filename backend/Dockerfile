FROM python:3.11-slim
WORKDIR /app
COPY . .
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install -r /tmp/requirements.txt

RUN chmod +x entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
