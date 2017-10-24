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
    USER_TYPE_FACEBOOK = 'F'
    USER_TYPE_DJANGO = 'D'
    CHOICES_USER_TYPE = (
        (USER_TYPE_FACEBOOK, 'Facebook'),
        (USER_TYPE_DJANGO, 'Django'),
    )
    user_type = models.CharField(max_length=1, choices=CHOICES_USER_TYPE)
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
    )

    objects = UserManager()  # proxy model로 UserManager 사용한다.

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = ''

    # def follow_toggle(self, user):
    #     if not isinstance(user, User):
    #         raise ValueError('"user" argument must be User instance!')
    #
    #     # 사용자가 팔로우 하는 목록에 해당 사용자가 존재 하면, 그 팔로우 관계를 삭제한다.
    #     if user in self.following_users.all():
    #         Relation.objects.filter(
    #             who_follows=self,
    #             who_is_followed=user,
    #         ).delete()
    #     else:
    #         Relation.objects.create(
    #             who_follows=self,
    #             who_is_followed=user,
    #         )

    def follow_toggle(self, user):
        # 1. 주어진 user가 User객체인지 확인
        #    아니면 raise ValueError()
        # 2. 주어진 user를 follow하고 있으면 해제
        #    안 하고 있으면 follow함
        if not isinstance(user, User):
            raise ValueError('"user" argument must be User instance!')

        relation, relation_created = self.following_users.who_follows.get_or_create(follower=user)
        if relation_created:
            return True
        relation.delete()
        return False

        # if user in self.following_users.all():
        #     Relation.objects.filter(
        #         from_user=self,
        #         to_user=user,
        #     ).delete()
        # else:
        #     # Relation중개모델을 직접 사용하는 방법
        #     Relation.objects.create(
        #         from_user=self,
        #         to_user=user,
        #     )
        #     # Relation에 대한역참조 매니저를 사용하는 방법
        #     self.following_user_relations.create(to_user=user)


class Relation(models.Model):
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="who_follows"
    )
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="who_is_followed"
    )
    created_time = models.DateTimeField(auto_now=True)
