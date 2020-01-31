FROM            python:3.7-slim

COPY            ./requirements.txt /tmp/
RUN             pip install -r /tmp/requirements.txt

COPY            . /src/Todoapp
WORKDIR         /src/Todoapp/app
CMD             ./manage.py runserver 0:8000
