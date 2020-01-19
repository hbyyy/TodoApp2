from django.urls import path

from todos.views import todolist_view, todo_create

app_name = 'todos'
urlpatterns = [
    path('', todolist_view, name='todo-list'),
    path('create/', todo_create, name='todo-create')
]
