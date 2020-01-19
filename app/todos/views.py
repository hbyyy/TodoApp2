from django.shortcuts import render, redirect

# Create your views here.
from django.utils import timezone

from todos.forms import TodosForm
from todos.models import Todo


def todolist_view(request):
    todos = Todo.objects.filter(user=request.user
                                ).filter(created_date__day=timezone.localtime().day
                                         ).order_by('created_date')
    form = TodosForm()
    context = {
        'form': form,
        'todos': todos,
        'time': timezone.localtime()
    }
    return render(request, 'todos/main.html', context)


def todo_create(request):
    if request.method == 'POST':
        form = TodosForm(data=request.POST)
        if form.is_valid():
            form.save(request.user.id)
        return redirect('todos:todo-list')
