import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from config import settings
from .forms import SignUpForm, LoginForm

from django.contrib.auth import get_user_model, logout as django_logout

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
        'facebook_app_id': settings.FACEBOOK_APP_ID
    }
    return render(request, 'member/login.html', context)


def facebook_login(request):
    url_access_token = 'https://graph.facebook.com/v2.10/oauth/access_token?'

    redirect_uri = '{scheme}://{host}{relative_url}'.format(
        scheme=request.scheme,
        host=request.META['HTTP_HOST'],
        relative_url=reverse('member:facebook_login')
    )

    params_access_token = {
        'client_id': settings.FACEBOOK_APP_ID,
        'client_secret': settings.FACEBOOK_SECRET_KEY,
        'redirect_uri': redirect_uri,
        'code': request.GET.get('code'),
    }

    r = requests.get(url_access_token, params_access_token)

    return HttpResponse(r.text)


def logout(request):
    django_logout(request)

    return redirect('member:login')
