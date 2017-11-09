from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from ..apis import PostList

urlpatterns = [
    url(r'^post/$', PostList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)