from django.conf.urls import url, include

from member.apis import Login, Signup, FacebookLogin
from post.apis import PostList

urlpatterns = [
    url(r'^member/', include('member.urls.apis', namespace='api-member')),
    url(r'^post/', include('post.urls.apis', namespace='api-post')),
]
