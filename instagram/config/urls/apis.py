from django.conf.urls import url, include

from member.apis import Login, Signup, FacebookLogin
from post.apis import PostList
from utils import apis

urlpatterns = [
    url(r'^member/', include('member.urls.apis', namespace='api-member')),
    url(r'^post/', include('post.urls.apis', namespace='api-post')),
    url(r'^utils/sms/send/$', apis.SendSMS.as_view(), name='send-SMS')
]
