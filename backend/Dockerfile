FROM python:3.9-slim
WORKDIR /app
COPY /backend/ /app/
RUN pip3 install -r requirements.txt --no-cache-dir
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
