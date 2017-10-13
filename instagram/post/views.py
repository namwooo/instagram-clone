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


def upload_photo(request):
    if request.method == 'POST':
        photo = request.FILES['myphoto']
        Post.objects.create(photo=photo)

        return HttpResponse('photo uploaded success')

    return render(request, 'post/post_list.html')

