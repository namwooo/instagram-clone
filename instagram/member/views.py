from django.shortcuts import render, redirect

from .forms import SignUpForm, LoginForm

from django.contrib.auth import get_user_model

User = get_user_model()


def signup(request):
    if request.method == 'POST':
        # 데이터가 바인딩된 SignUpForm인스턴스를 생성한다.
        form = SignUpForm(request.POST)

        # 해당 form이 자신의 필드에 유효한 데이터인지 검사한다.
        if form.is_valid():
            new_user = form.signup()

            return redirect('/member/login/')

    else:
        # 빈 form을 생성하여 재사용한다.
        form = SignUpForm()

    context = {
        'form': form
    }

    return render(request, 'member/signup.html', context)


def login(request):
    # 요청이 POST 메소드인지 검사한다.
    if request.method == 'POST':
        # 데이터가 바인딩된 LoginForm인스턴스를 생성한다.
        form = LoginForm(request.POST)
        # 해당 form이 자신의 필드에 유효한지 검사하고, cleaned_data로 데이터를 가지고 온다.
        if form.is_valid():
            # form에 login 메소드를 사용하여 로그인 한다.
            form.login(request)

            return redirect('/post/')
    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'member/login.html', context)
