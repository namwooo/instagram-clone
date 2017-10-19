from django.conf.urls import url

from .views import comment_create, post_detail, post_create, post_list

urlpatterns = [
    url(r'^$', post_list, name='post_list'),
    url(r'^create/$', post_create, name='post_create'),
    url(r'^(?P<post_pk>\d+)/$', post_detail, name='post_detail'),
    url(r'^(?P<post_pk>\d+)/comment/$', comment_create, name='comment_create'),
]