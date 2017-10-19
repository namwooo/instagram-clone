from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=50, blank=True)
    photo = models.ImageField(upload_to='post')
    created_date = models.DateTimeField(auto_now_add=True)


class PostComment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_date']
