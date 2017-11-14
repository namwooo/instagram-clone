from django.conf.urls import url

from ..apis import PostList, PostDetail

urlpatterns =[
    url(r'^$', PostList.as_view(), name='api-post'),
    url(r'^(?P<pk>\d+)/$', PostDetail.as_view(), name='api-post-detail'),
]
