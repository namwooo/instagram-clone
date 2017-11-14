from django.core.exceptions import PermissionDenied

from django.shortcuts import get_object_or_404, redirect

from ..models import Post, PostComment
from ..forms import CommentForm


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
            next_path = request.GET.get('next')
            if next_path:
                return redirect(next_path)
        else:
            raise PermissionDenied
