from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

# Create your views here.
from members.forms import LoginForm, SignupForm
from members.models import User
from members.oauth import get_secret, naver_login_url, naver_token_request


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.authenticate(request)
            login(request, user)
            return redirect('todos:todo-list')
    else:
        form = LoginForm()

    secret = get_secret()
    request_url = naver_login_url(
        client_id=secret['NAVER_CLIENT_ID'],
        redirect_url='http://localhost:8000/naver-login',
        state='RANDOM_STATE'
    )
    context = {
        'login_form': form,
        'request_url': request_url
    }
    return render(request, 'members/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


def naver_login_view(request):
    code = request.GET['code']
    state = request.GET['state']

    secret = get_secret()
    response = naver_token_request(
        client_id=secret['NAVER_CLIENT_ID'],
        client_secret_key=secret['NAVER_CLIENT_SECRET_KEY'],
        code=code,
        state=state
    )

    id = response.json()['response']['id']
    user = User.objects.get(username=id)
    login(request, user)
    return redirect('todos:todo-list')


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            login(request, user)
            return redirect('todos:todo-list')
    else:
        form = SignupForm()

    secret = get_secret()
    request_url = naver_login_url(
        client_id=secret['NAVER_CLIENT_ID'],
        redirect_url='http://localhost:8000/members/naver-signup',
        state='RANDOM_STATE'
    )

    context = {
        'signup_form': form,
        'request_url': request_url
    }
    return render(request, 'members/signup.html', context)


def naver_signup_view(request):
    code = request.GET['code']
    state = request.GET['state']

    secret = get_secret()
    response = naver_token_request(
        client_id=secret['NAVER_CLIENT_ID'],
        client_secret_key=secret['NAVER_CLIENT_SECRET_KEY'],
        code=code,
        state=state
    )

    id = response.json()['response']['id']
    name = response.json()['response']['name']

    user = User.objects.create_user(
        username=id,
        name=name,
        type='N'

    )

    login(request, user)
    return redirect('todos:todo-list')
