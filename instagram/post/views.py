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


def post_create(request):
    """
    사용자로 부터 입력 받은 이미지 파일을 media/post에 저장하고,
    그 파일 위치 정보를 데이터 베이스에 저장한다.
    :param request: request to upload imagefile
    :return: render to post_create.html
    """
    if request.method == 'POST':
        # POST 요청의 경우 PostForm인스턴스 생성과정에서 request.POST, request.FILES 사용
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post.objects.create(photo=form.cleaned_data['photo'])
            return HttpResponse(f'<img src="{post.photo.url}">')
    else:
        form = PostForm()

    context = {
        'form': form
    }

    return render(request, 'post/post_create.html', context)


def post_detail(request, post_pk):
    """
    사용자가 원하는 하나의 포스트만을 보여준다.
    :param request: request to display post details
    :param post_pk: the post's primary key to access the post
    :return: render to post_detail.html
    """
    post = get_object_or_404(Post, pk=post_pk)  # Post 객체가 없을 경우, 404 에러가 발생한다.
    comment_form = CommentForm()

    context = {
        'post': post,
        'comment_form': comment_form
    }

    return render(request, 'post/post_detail.html', context)


def comment_create(request, post_pk):
    """
    포스트에 댓글을 생성한다.
    댓글 생성 후, 해당 포스트 댓글 맨 위를 사용자에게 보여준다. post_list.html에서
    /post/#post-comments-{{ post.pk }}를 request로 가져와 next에 할당한다.
    id가 post-comments-{{ post.pk }}인 html위치로 리다이렉트 한다.
    :param request:
    :param post_pk:
    :return:
    """
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            PostComment.objects.create(
                post=post,
                content=form.cleaned_data['comment']
            )
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect('post_detail', post_pk=post.pk)
