from django.shortcuts import render, get_object_or_404, redirect

from .models import Post, PostComment
from .forms import PostForm, CommentForm


def post_list(request):
    """
    author가 없는 포스트를 제외한 Post목록을 반환한다.
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
    if not request.user.is_authenticated:
        return redirect('member:login')

    if request.method == 'POST':
        # POST 요청의 경우 PostForm인스턴스 생성과정에서 request.POST, request.FILES 사용
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post.objects.create(photo=form.cleaned_data['photo'], author=request.user)
            return redirect('post:post_list')
    else:
        form = PostForm()

    context = {
        'form': form
    }

    return render(request, 'post/post_create.html', context)


# def post_delete(request, post_pk):
#     if not request.user.is_authenticated:
#         return redirect('post:post_list')
#
#     if request.method == 'POST':
#         Post.objects.get(pk=post_pk).delete()
#     return redirect('post:post_list')


def post_detail(request, post_pk):
    """
    사용자가 원하는 하나의 포스트만을 보여준다.
    :param request: request to display post details from user
    :param post_pk: post's primary key to access a certain post
    :return: render to post_detail.html
    """
    # Post 객체가 없을 경우, 404 에러가 발생한다.
    post = get_object_or_404(Post, pk=post_pk)
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
    :param request:request to put comment on a post
    :param post_pk: post's primary key to access a post
    :return: redirect to post_detail.html
    """
    if not request.user.is_authenticated:
        return redirect('member:login')

    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            PostComment.objects.create(
                post=post,
                author=request.user,
                content=form.cleaned_data['comment']
            )
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect('post:post_detail', post_pk=post.pk)


# def comment_delete(request, post_pk):
#     if not request.user.is_authenticated:
#         return redirect('member:post_list')
#
#     if request.method == 'POST':
#         PostComment.objects.get(pk=post_pk).delete()
#     return redirect('post:post_list')
