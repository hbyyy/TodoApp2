daemon = False
chdir = '/srv/Todoapp/app'
bind = 'unix:/run/todos.sock'
accesslog = '/var/log/gunicorn/todos-access.log'
errorlog = '/var/log/gunicorn/todos-error.log'
capture_output = True
