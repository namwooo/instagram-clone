from django.conf.urls import url

from .views import signup, login, logout, facebook_login, FrontFacebookLogin

urlpatterns = [
    url(r'^signup/$', signup, name='signup'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^facebook-login/$', facebook_login, name='facebook_login'),
    url(r'^front-facebook-login/$', FrontFacebookLogin.as_view(), name='front-facebook-login'),
]
