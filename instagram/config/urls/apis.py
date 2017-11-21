from django.conf.urls import url, include

from sms import apis

urlpatterns = [
    url(r'^member/', include('member.urls.apis', namespace='api-member')),
    url(r'^post/', include('post.urls.apis', namespace='api-post')),
    url(r'^sms/', include('sms.urls', namespace='api-sms')),
]
