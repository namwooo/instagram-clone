from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models

from post.models import Post


class UserManager(DjangoUserManager):
    """
    superuser 생성시, age 디폴트 값을 29으로 할당한다.
    auth.UserManager.create_superuser를 오버라이드했다.
    """

    def create_superuser(self, *args, **kwargs):
        return super().create_superuser(age=29, *args, **kwargs)


class User(AbstractUser):
    """
    AbstractUser모델을 상속 받은 User 모덿을 정의한다.
    Username과 password는 필수 사항이다. img_profile과 age는 선택사항이다.
    그외 선택사항들은 AbstractUser모델을 참고하자.
    """
    img_profile = models.ImageField(
        upload_to='user',
        blank=True,
    )
    age = models.IntegerField()
    like_posts = models.ManyToManyField(
        'post.Post',
        verbose_name='좋아요 누른 포스트 목록'
    )
    following_users = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='Relation',
        related_name='followers'
    )

    objects = UserManager()  # proxy model로 UserManager 사용한다.

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = ''


class Relation(models.Model):
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="who_follows")
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="who_is_followed")
    created_time = models.DateTimeField(auto_now=True)
