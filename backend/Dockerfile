FROM python:3.9-slim
WORKDIR /app
COPY /backend/requirements.txt /app/
RUN pip3 install -r requirements.txt --no-cache-dir
COPY /backend/ /app/
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
