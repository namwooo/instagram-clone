from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import SignUpForm

from django.contrib.auth import get_user_model

User = get_user_model()


def signup(request):
    if request.method == 'POST':
        # 데이터가 바인딩된 SignUpForm인스턴스를 생성
        form = SignUpForm(request.POST)
        # 해당 form이 자신의 필드에 유효한 데이터인지 검사
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            new_user = User.objects.create_user(first_name=first_name,
                                                last_name=last_name,
                                                username=username,
                                                password=password,
                                                email=email)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

            return redirect('/post/')
    else:
        form = SignUpForm()

    context = {
        'form': form
    }

    return render(request, 'member/signup.html', context)


def login(request):
    if request.metho == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
        else:
            return redirect('/post/')

    else:
        return render(request, 'member/login.html')
