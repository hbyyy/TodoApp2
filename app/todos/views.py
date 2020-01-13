from django.shortcuts import render


# Create your views here.


def todolist_view(request):
    context = {
        'user': request.user
    }
    return render(request, 'todos/main.html')
