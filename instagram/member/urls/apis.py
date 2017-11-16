from django.conf.urls import url

from ..apis import Login, Signup, FacebookLogin

urlpatterns = [
    url(r'^login/$', Login.as_view(), name='api-login'),
    url(r'^signup/$', Signup.as_view(), name='api-signup'),
    url(r'facebook-login/$', FacebookLogin.as_view(), name='api-facebook-login')
]
