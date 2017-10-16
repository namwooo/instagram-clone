from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user.save()

        return HttpResponse(f'{user.username}{user.password}')

    return render(request, 'member/signup.html')