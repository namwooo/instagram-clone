from django.http import HttpResponse
from django.shortcuts import render

from .models import Post
from .forms import PostForm


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
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post.objects.create(photo=form.cleaned_data['photo'])
            return HttpResponse(f'<img src="{post.photo.url}">')
    else:
        form = PostForm()

    return render(request, 'post/post_create.html', {'form': form})
