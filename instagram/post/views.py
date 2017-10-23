
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from member.decorators import login_required
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
    로그인된 사용자로 부터 이미지 파일과 author를 입력 받아, Post 객체를 생성한다.
    이미지 파일을 media/post에 저장된다.
    :param request: request to upload imagefile
    :return: render to post_create.html
    """
    if not request.user.is_authenticated:
        return redirect('member:login')

    if request.method == 'POST':
        # POST 요청의 경우 PostForm인스턴스 생성과정에서 request.POST, request.FILES 사용
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post:post_list')
    else:
        form = PostForm()

    context = {
        'form': form
    }

    return render(request, 'post/post_create.html', context)


def post_delete(request, post_pk):
    """
    사용자 이름과 포스트 작성자가 같을 때 해당 포스트를 삭제한다.
    :param request: request to delete a post from user
    :param post_pk: post's primary key to access a certain post
    :return: redirect to post_list.html
    """
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        if post.author == request.user:
            post.delete()
        else:
            raise PermissionDenied
    return redirect('post:post_list')


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
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect('post:post_detail', post_pk=post.pk)


def comment_delete(request, comment_pk):
    """
    로그인 된 사용자가 해당 댓글을 삭제한다.
    댓글 삭제 후, id가 post-comments-{{ post.pk }}인 html위치로 리다이렉트 한다.
    :param request: request to delete a comment from user
    :param comment_pk: PostComment's primary key
    :return: redirect to post_list/ redirect to html with id='next'
    """
    if request.method == 'POST':
        comment = get_object_or_404(PostComment, pk=comment_pk)
        if comment.author == request.user:
            comment.delete()
            next = request.GET.get('next')
            if next:
                return redirect('next')
        else:
            raise PermissionDenied

            # if not request.user.is_authenticated:
            #     return redirect('post:post_list')
            #
            # if request.method == 'POST':
            #     PostComment.objects.get(pk=comment_pk).delete()
            #     next = request.GET.get('next')  # next = post-comments-{{ post.pk }}
            #     if next:
            #         return redirect('next')
            #     return redirect('post:post_list')post_list


@login_required
def post_like_toggle(request, post_pk):
    """

    :param request:
    :param post_pk:
    :return:
    """
    if not request.user.is_authenticated:
        return redirect('member:login')

    if request.method == 'POST':
        next_path = request.GET.get('next')
        post = get_object_or_404(Post, pk=post_pk)
        user = request.user
        filtered_like_posts = user.like_posts.filter(pk=post_pk)

        if filtered_like_posts.exists():
            user.like_posts.remove(post)
        else:
            user.like_posts.add(post)

        if next_path:
            return redirect(next_path)
        return redirect('post:post_detail', post_pk=post_pk)