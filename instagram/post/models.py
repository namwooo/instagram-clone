from django.conf import settings
from django.db import models


class PostManager(models.Model):
    """
    Manager.get_queryset()을 오버라이드 하는 PostManager를 정의한다.
    get_queryset메소드는 author가 null인 객체를 제외한 모든 객체를 기지고 온다.
    """
    def get_queryset(self):
        return super().get_queryset().exclude(author__isnull=True)


class Post(models.Model):
    """
    photo와 create_date는 필수 사항이고, author는 선택 사항이다.
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    photo = models.ImageField(upload_to='post')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']

    objects = PostManager() # author가 null인 객체를 제외하는 매니저이다.


class PostComment(models.Model):
    """
    Post모델과 일대다 관계이다.
    content와 created_date는 필수 사항이고, author는 선택 사항이다.
    """
    post = models.ForeignKey(Post, related_name='comments')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_date']