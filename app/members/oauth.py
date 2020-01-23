import json
import os
from urllib.parse import urlunparse, urlparse, urlencode

import requests



def get_secret():
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'secrets.json'), 'r') as secret_json:
        return json.load(secret_json)


def naver_login_url(client_id, redirect_url, state):
    base_url = 'https://nid.naver.com/oauth2.0/authorize'
    url_params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_url,
        'state': state,
    }
    url = '{base}?{query}'.format(
        base=base_url,
        query='&'.join([f'{key}={value}' for key, value in url_params.items()])
    )
    return url


def facebook_login_url(client_id, redirect_url, state):
    base_url = 'https://www.facebook.com/v5.0/dialog/oauth?'
    query = {
        'client_id': client_id,
        'redirect_uri': redirect_url,
        'state': state,
    }
    url = '{base}{query}'.format(
        base=base_url,
        query='&'.join([f'{key}={value}' for key, value in query.items()])
    )
    return url


def naver_token_request(client_id, client_secret_key, code, state):
    base_url = 'https://nid.naver.com/oauth2.0/token'
    query = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret_key,
        'code': code,
        'state': state,

    }

    request_url = urlparse(base_url)._replace(query=urlencode(query))
    request_url = urlunparse(request_url)

    response = requests.get(request_url)
    access_token = response.json()['access_token']

    profile_api_request_url = 'https://openapi.naver.com/v1/nid/me'
    response = requests.get(profile_api_request_url, headers={
        'Authorization': f'Bearer {access_token}'
    })
    return response


def facebook_token_request(client_id, client_secret_key, redirect_uri, code):
    base_url = 'https://graph.facebook.com/v5.0/oauth/access_token?'
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'client_secret': client_secret_key,
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
    return response