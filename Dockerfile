FROM            python:3.7-slim

RUN             apt -y update && apt -y dist-upgrade
RUN             apt -y install nginx
COPY            ./requirements.txt /tmp/
RUN             pip install -r /tmp/requirements.txt

COPY            . /srv/Todoapp
WORKDIR         /srv/Todoapp/app

RUN             mkdir /var/log/gunicorn
RUN             cp /srv/Todoapp/.config/todos.nginx /etc/nginx/sites-enabled/
