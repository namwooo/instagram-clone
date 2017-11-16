from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect

from member.decorators import login_required
from ..models import Post
from ..forms import PostForm, CommentForm


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


@login_required
def post_like_toggle(request, post_pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        user = request.user
        filtered_like_posts = user.like_posts.filter(pk=post_pk)
        next_path = request.GET.get('next')

        if filtered_like_posts.exists():
            user.like_posts.remove(post)
        else:
            user.like_posts.add(post)

        if next_path:
            return redirect(next_path)
        return redirect('post:post_detail', pk=post_pk)
