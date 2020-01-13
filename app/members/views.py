from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from members.forms import LoginForm, SignupForm
from members.models import User


def login_view(request):
    form = LoginForm()
    context = {
        'login_form': form
    }
    return render(request, 'members/login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            login(request, user)
            # return render()
            return HttpResponse(f'{request.user.username}, {request.user.password} login')
    else:
        form = SignupForm()

    context = {
        'signup_form': form
    }
    return render(request, 'members/signup.html', context)
