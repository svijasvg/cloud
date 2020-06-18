#———————————————————————————————————————— HomePageView.py

from django.shortcuts import get_object_or_404
from svija.models import Prefix, Settings
from svija.views import PageView
from modules import cache_functions

@cache_functions.cache_per_user_function(ttl=60*60*24, cache_post=False)
def HomePageView(request, path1):

    if path1 == '':
        settings = get_object_or_404(Settings,active=True)
        path1 = settings.prefix.path

    prefix = get_object_or_404(Prefix, path=path1)
    path2 = prefix.default

    response = PageView(request, path1, path2,)
    return response

#———————————————————————————————————————— fin
