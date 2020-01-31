from django.urls import path

from todos.views import todolist_view, todo_create, todo_finish_view, todo_cancel_view

app_name = 'todos'
urlpatterns = [
    path('', todolist_view, name='todo-list'),
    path('create/', todo_create, name='todo-create'),
    path('finish/<int:todo_id>', todo_finish_view, name='todo-finish'),
    path('cancel/<int:todo_id>', todo_cancel_view, name='todo-cancel'),
]
