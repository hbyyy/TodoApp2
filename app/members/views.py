from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from members.forms import LoginForm, SignupForm


def login_view(request):
    form = LoginForm()
    context = {
        'login_form': form
    }
    return render(request, 'members/login.html', context)


def signup_view(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)

    else:
        form = SignupForm()

    context = {
        'signup_form': form
    }
    return render(request, 'members/signup.html', context)
