from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Post, PostComment
from .forms import PostForm, CommentForm


def post_list(request):
    """
    모든 Post목록을 반환한다.
    빈 CommentFor인스턴스를 같이 반환하여 post_list.html에서 form태그를 대체한다.
    :param request: request to list all posts
    :return: render to post_list.html
    """
    posts = Post.objects.all()
    comment_form = CommentForm()

    context = {
        'posts': posts,
        'comment_form': comment_form,
    }

    return render(request, 'post/post_list.html', context)


# def post_create(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post =  Post.objects.create(photo=form.cleaned_data['photo'])
#             return


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


def post_detail(request, post_pk):
    """
    1. 요청 받은 request와 pk로 해당 post 객체를 post에 할당
    2.
    :param request:
    :return:
    """
    post = Post.objects.get(pk=post_pk)
    post = get_object_or_404(Post, pk=post_pk)
    comment_form = CommentForm()
    context = {
        'post': post,
        'comment_form': comment_form

    }
    return render(request, 'post/post_detail.html', context)


def comment_create(request, post_pk):
    """

    :param request:
    :return:
    """
    # 'post_pk'에 해당하는 Post 인스턴스를  post에 할당
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        # 데이터가 바인딩된 CommentForm 인스턴스를 form에 할당
        form = CommentForm(request.POST)
        # 유효성 검사
        if form.is_valid():
            PostComment.objects.create(
                post=post,
                content=form.cleaned_data['comment']
            )
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect('post_detail', post_pk=post.pk)
