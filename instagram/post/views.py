from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render

from .models import Post


def post_list(request):
    """
    모든 Post목록을 리턴
    template은 'post/post_list.html'을 사용
    :param request:
    :return:
    """
    posts = Post.objects.all()
    context = {
        'posts': posts
    }

    return render(request, 'post/post_list.html', context)


def post_create(request):
    """
    1. post_create.html 파일을 만들고 /post/create
    :param request:
    :return:
    """
    if request.method == 'POST':
        photo = request.FILES['photo']
        Post.objects.create(photo=photo)

        return HttpResponse('photo uploaded success')

    else:
        return render(request, 'post/post_create.html')

