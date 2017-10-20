from django.shortcuts import render, redirect

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

            return redirect('post:post_list')
    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'member/login.html', context)


def logout(request):
    django_logout(request)

    return redirect('member:login')
