from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models


class UserManager(DjangoUserManager):
    def create_superuser(self, *args, **kwargs):
        return super().create_superuser(age=29, *args, **kwargs)


class User(AbstractUser):
    objects = UserManager() # proxy model로 UserManager 사용한다.

    img_profile = models.ImageField(
        upload_to='user',
        blank=True,
    )
    age = models.IntegerField()
    # REQUIRED_FIELDS에 AbstractUser의 REQUIRED_FIELDS와 age를 할당한다.
    # REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS + ['age']
