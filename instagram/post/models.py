from django.db import models

"""
post앱 생성
class Post(models.Model):
    photo = models.어떤 필드를 써야 할까
    생성 날짜 기록

class PostComment:
    post = 자신의 Post와 MTO으로 연결
    생성일시 기록
"""


class Post(models.Model):
    title = models.CharField(max_length=50, blank=True)
    photo = models.ImageField(upload_to='post')
    created_date = models.DateTimeField(auto_now_add=True)


class PostComment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
