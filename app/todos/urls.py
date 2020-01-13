from django.urls import path

from todos.views import todolist_view

app_name = 'todos'
urlpatterns = [
    path('', todolist_view, name='todolist'),
]
