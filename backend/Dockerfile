FROM python:3.11-slim
WORKDIR /app
COPY /backend/requirements.txt /app/
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /app/
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
