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
        # POST 요청의 경우 PostForm인스턴스 생성과정에서 request.POST, request.FILES 사용
        form = PostForm(request.POST, request.FILES)
        # form에 전달 된 데이터들이 Form field에 대해 유효 한지 검사
        if form.is_valid():
            # 유효할 경우 Post 인스턴스 생성 및 저장
            post = Post.objects.create(photo=form.cleaned_data['photo'])
            return HttpResponse(f'<img src="{post.photo.url}">')
    else:
        # GET 요청의 겨우 빈 form 인스턴스를 생성
        form = PostForm()

    context = {
        'form': form
    }

    return render(request, 'post/post_create.html', context)


def post_detail(request, pk):
    """
    1. 요청 받은 request와 pk로 해당 post 객체를 post에 할당
    2.
    :param request:
    :return:
    """
    post = Post.objects.get(pk=pk)
    context = {
        'post': post
    }
    return render(request, 'post/post_detail.html', context)
