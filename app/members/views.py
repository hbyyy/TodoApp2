from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

# Create your views here.
from members.forms import LoginForm, SignupForm
from members.models import User
from members.oauth import get_secret, naver_login_url, naver_token_request, facebook_login_url, facebook_token_request


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
        redirect_url='https://hbyyytodo.xyz/naver-login',
        state='RANDOM_STATE'
    )

    facebook_request_url = facebook_login_url(
        client_id=secret['FACEBOOK_CLIENT_ID'],
        redirect_url='https://hbyyytodo.xyz/facebook-login',
        state='RANDOM_STATE'
    )

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

    user = User.objects.get(username=response.json()['response']['id'])
    login(request, user)
    return redirect('todos:todo-list')


def facebook_login_view(request):
    code = request.GET['code']

    secret = get_secret()

    response = facebook_token_request(
        client_id=secret['FACEBOOK_CLIENT_ID'],
        client_secret_key=secret['FACEBOOK_CLIENT_SECRET_KEY'],
        redirect_uri='https://hbyyytodo.xyz/facebook-login',
        code=code
    )

    user = User.objects.get(username=response.json()['id'])
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
    naver_request_url = naver_login_url(
        client_id=secret['NAVER_CLIENT_ID'],
        redirect_url='https://hbyyytodo.xyz/members/naver-signup',
        state='RANDOM_STATE'
    )

    facebook_request_url = facebook_login_url(
        client_id=secret['FACEBOOK_CLIENT_ID'],
        redirect_url='https://hbyyytodo.xyz/members/facebook-signup',
        state='RANDOM_STATE'
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

    secret = get_secret()

    response = facebook_token_request(
        client_id=secret['FACEBOOK_CLIENT_ID'],
        client_secret_key=secret['FACEBOOK_CLIENT_SECRET_KEY'],
        redirect_uri='https://hbyyytodo.xyz/members/facebook-signup',
        code=code
    )

    user = User.objects.create_user(
        username=response.json()['id'],
        name=response.json()['name'],
        type='F',
    )

    login(request, user)
    return redirect('todos:todo-list')
