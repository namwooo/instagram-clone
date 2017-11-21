from django.conf.urls import url

from .apis import SendSMS

urlpatterns =[
    url(r'send-sms/$', SendSMS.as_view(), name='send-sms')
]
