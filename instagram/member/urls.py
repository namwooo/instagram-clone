from django.conf.urls import url

from .views import signup, login

urlpatterns = [
    url(r'^signup/$', signup, name='signup'),
    url(r'^login/$', login, name='login'),
]
