FROM python:3.10-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
RUN apt-get update -y
ADD . /code/
WORKDIR /code


RUN rm -rf */migrations/
RUN rm -rf */*/migrations/
RUN rm -rf db.sqlite3
# RUN pip install django-extensions
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y nano cron at && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt

# Set up entrypoint script
RUN echo "#!/bin/sh\n\
service cron start\n\
service atd start\n\
touch /code/logs.log\n\
crontab 0 * * * * /usr/local/bin/python /code/clean_up.py >> /code/logs.log 2>&1\n\
gunicorn -c gunicorn.py collector.wsgi:application -b ${1:-0.0.0.0}:${2:-8000} --preload --timeout ${3:-600}\n" > /code/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /code/entrypoint.sh

# Set the entrypoint script as the default command
CMD ["/code/entrypoint.sh"] 