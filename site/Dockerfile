FROM "python:3.9.18-alpine3.18"

RUN ["mkdir", "-p", "app"]
COPY . /app
COPY ./crontab /etc/

RUN ["pip3", "install", "-r", "/app/requirements.txt"]

CMD ["hypercorn", ""]
