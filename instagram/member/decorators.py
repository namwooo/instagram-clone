from urllib.parse import urlparse

from django.shortcuts import redirect
from django.urls import reverse


def login_required(view_func, next_url=None):
    def decorator(*args, **kwargs):
        request = args[0]
        if not request.user.is_authenticated:
            referer = urlparse(request.META['HTTP_REFERER'])
            url = '{base_url}?next={referer}'.format(
                base_url=reverse('memeber:login'),
                referer=referer)

            return redirect('member:login')
        return view_func(*args, **kwargs)

    return decorator
