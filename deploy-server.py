#!/usr/bin/env python

import os
import subprocess
from pathlib import Path

HOME = str(Path.home())
IDENTITY_FILE = os.path.join(HOME, '.ssh', 'todoapp.pem')
HOST = '13.125.186.75'
USER = 'ubuntu'
TARGET = f'{USER}@{HOST}'
SECRETS_FILE = os.path.join(HOME, 'projects', 'wps12th', 'djangoProject', 'Todoapp2', 'app', 'secrets.json')


def run(cmd):
    subprocess.run(cmd, shell=True)


def ssh_run(cmd):
    run(f"ssh -i {IDENTITY_FILE} {TARGET} -C '{cmd}'")


def server_init():
    print('============================server_init========================================')
    ssh_run(f'sudo apt -y update && sudo apt -y dist-upgrade && sudo apt -y autoremove')
    ssh_run(f'sudo apt -y install docker.io')


def requirements_update():
    print('============================requirements_update========================================')
    run(f'poetry export -f requirements.txt > requirements.txt ')


def docker_update():
    print('============================docker_update========================================')
    run(f'docker build -t lloasd33/todos -f Dockerfile .')
    run(f'docker push lloasd33/todos')


def server_pull_run():
    print('============================server_pull_run========================================')
    ssh_run(f'docker stop todos')
    ssh_run(f'docker pull lloasd33/todos')
    ssh_run(f'docker run --rm -it -d -p 80:80 --name todos lloasd33/todos /bin/bash')


def copy_secret():
    print('============================copy_secret========================================')
    run(f'scp -i {IDENTITY_FILE} {SECRETS_FILE} {TARGET}:/tmp')
    ssh_run(f'docker cp /tmp/secrets.json todos:/srv/Todoapp/app')


def run_server():
    print('============================run_server========================================')
    # ssh_run(f'docker exec -it -d todos gunicorn -b unix:/run/todos.sock config.wsgi')
    # ssh_run(f'docker exec -it -d todos nginx -g "daemon off;"')
    ssh_run(f'docker exec -it -d todos supervisord -c ../.config/supervisord.conf -n')


if __name__ == '__main__':
    server_init()
    requirements_update()
    docker_update()
    server_pull_run()
    copy_secret()
    run_server()