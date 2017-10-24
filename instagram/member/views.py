from typing import NamedTuple

import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from config import settings
from .forms import SignUpForm, LoginForm

from django.contrib.auth import get_user_model, logout as django_logout, login as django_login

User = get_user_model()


def signup(request):
    """
    사용자가 입력한 데이터가 바인딩된 SignUpForm 인스턴스를 생성한다.
    해당 form 인스턴스에 대해 유효성을 검사한다.
    성공한 경우 로그인 페이지로 리다이렉트, 실패한 경우 회원가입 페이지로 렌더링한다.
    :param request: request for post from user
    :return: render to signup.html
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return redirect('member:login')
    else:
        form = SignUpForm()

    context = {
        'form': form
    }

    return render(request, 'member/signup.html', context)


def login(request):
    """
    사용자가 입력한 데이터가 바인딩된 LoginForm 인스턴스를 생성한다.
    해당 form 인스턴스에 대해 유효성을 검사한다.
    성공한 경우 포스트 페이지로 리다이렉트, 실패한 경우 로그인 페이지로 렌더링한다.
    :param request: request for login from user
    :return: render to login.html
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            next_path = request.GET.get('next')
            if next_path:
                return redirect('next_path')
            return redirect('post:post_list')
    else:
        form = LoginForm()

    context = {
        'form': form,
        'facebook_app_id': settings.FACEBOOK_APP_ID,
        'facebook_scope': settings.FACEBOOK_SCOPE,
    }
    return render(request, 'member/login.html', context)


def facebook_login(request):
    class AccessTokenInfo(NamedTuple):
        access_token: str
        token_type: str
        expires_in: int

    class DebugTokenInfo(NamedTuple):
        app_id: str
        application: str
        expires_at: int
        is_valid: bool
        issued_at: int
        scopes: list
        type: str
        user_id: str

    class UserInfo:
        def __init__(self, data):
            self.id = data['id']
            self.email = data['email']
            self.url_picture = data['picture']['data']['url']

    app_id = settings.FACEBOOK_APP_ID
    app_secret_key = settings.FACEBOOK_SECRET_KEY
    app_access_token = f'{app_id}|{app_secret_key}'
    code = request.GET.get('code')

    def get_access_token_info(code):
        url_access_token = 'https://graph.facebook.com/v2.10/oauth/access_token'

        redirect_uri = '{scheme}://{host}{relative_url}'.format(
            scheme=request.scheme,
            host=request.META['HTTP_HOST'],
            relative_url=reverse('member:facebook_login')
        )

        params_access_token = {
            'client_id': app_id,
            'client_secret': app_secret_key,
            'redirect_uri': redirect_uri,
            'code': code,
        }

        response = requests.get(url_access_token, params_access_token)

        return AccessTokenInfo(**response.json())

    def get_debug_token_info(token):
        url_debug_token = 'https://graph.facebook.com/debug_token'
        params_debug_token = {
            'input_token': access_token,
            'access_token': app_access_token,
        }
        response = requests.get(url_debug_token, params_debug_token)

        return DebugTokenInfo(**response.json()['data'])

    access_token_info = get_access_token_info(code)
    access_token = access_token_info.access_token
    debug_token_info = get_debug_token_info(access_token)

    # 유저 정보 가져오기
    user_info_field = [
        'id',
        'name',
        'picture',
        'email',
    ]
    url_graph_user_info = 'https://graph.facebook.com/me'
    params_graph_user_info = {
        'fields': ','.join(user_info_field),
        'access_token': access_token,
    }
    response = requests.get(url_graph_user_info, params_graph_user_info)
    result = response.json()

    user_info = UserInfo(data=result)
    username = f'fb_{user_info.id}'
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
    else:
        user = User.objects.create_user(
            user_type=User.USER_TYPE_FACEBOOK,
            username=username,
            age=0,
        )
    django_login(request, user)
    return redirect('post:post_list')


def logout(request):
    django_logout(request)

    return redirect('member:login')
