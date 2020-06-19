#———————————————————————————————————————— HomePageView.py

from django.shortcuts import get_object_or_404
from svija.models import Prefix, Settings
from svija.views import PageView
from modules import cache_functions

@cache_functions.cache_per_user_function(ttl=60*60*24, cache_post=False)
def HomePageView(request, request_prefix):

    if request_prefix == '':
        settings = get_object_or_404(Settings,active=True)
        request_prefix = settings.prefix.path

    prefix = get_object_or_404(Prefix, path=request_prefix)
    request_slug = prefix.default

    response = PageView(request, request_prefix, request_slug,)
    return response

#———————————————————————————————————————— fin
