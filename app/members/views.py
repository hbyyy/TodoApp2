import requests
from django.contrib.auth import login, logout
from django.http import HttpResponse
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
    naver_request_url = naver_login_url(
        client_id=secret['NAVER_CLIENT_ID'],
        redirect_url='http://localhost:8000/naver-login',
        state='RANDOM_STATE'
    )
    facebook_request_url = ''
    context = {
        'login_form': form,
        'naver_request_url': naver_request_url,
        'facebook_request_url': facebook_request_url,
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


def facebook_login_view(request):
    pass


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
    naver_request_url = naver_login_url(
        client_id=secret['NAVER_CLIENT_ID'],
        redirect_url='http://localhost:8000/members/naver-signup',
        state='RANDOM_STATE'
    )

    base_url = 'https://www.facebook.com/v5.0/dialog/oauth?'
    query = {
        'client_id': secret['FACEBOOK_CLIENT_ID'],
        'redirect_uri': 'http://localhost:8000/members/facebook-signup',
        'state': 'RANDOM_STATE'
    }
    facebook_request_url = '{base}{query}'.format(
        base=base_url,
        query='&'.join([f'{key}={value}' for key, value in query.items()])
    )

    context = {
        'signup_form': form,
        'naver_request_url': naver_request_url,
        'facebook_request_url': facebook_request_url
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


def facebook_signup_view(request):
    code = request.GET['code']
    state = request.GET['state']

    secret = get_secret()

    base_url = 'https://graph.facebook.com/v5.0/oauth/access_token?'
    params = {
        'client_id': secret['FACEBOOK_CLIENT_ID'],
        'redirect_uri': 'http://localhost:8000/members/facebook-signup',
        'client_secret': secret['FACEBOOK_CLIENT_SECRET_KEY'],
        'code': code,
    }
    token_request_url = '{base}{query}'.format(
        base=base_url,
        query='&'.join([f'{key}={value}' for key, value in params.items()])
    )

    response = requests.get(token_request_url)

    access_token = response.json()['access_token']
    base_url = 'https://graph.facebook.com/me?'
    params = {
        'field': 'id,name',
        'access_token': access_token,
    }

    response = requests.get(base_url, params=params)

    user = User.objects.create_user(
        username=response.json()['id'],
        name=response.json()['name'],
        type='F',
    )

    login(request, user)
    return redirect('todos:todo-list')
