from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import MemberForm


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user.save()

        return HttpResponse(f'username:{user.username} password:{user.password}')

    return render(request, 'member/signup.html')


def signin(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            return redirect('/post/')

    return render(request, 'member/signin.html')
