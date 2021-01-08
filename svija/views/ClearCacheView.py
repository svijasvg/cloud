#———————————————————————————————————————— ClearCacheView.py
# /c clears cache, for admins only

from django.core.cache import cache as memcache
from django.http import HttpResponse
from svija.views import PageView

def ClearCacheView(request):
    if not request.user.is_superuser:
        response = PageView(request, 'en','missing',)
        response.status_code = 404
        return response

    memcache.clear()
    msg = "<html><body><script> alert('Cache deleted.'); window.history.go(-1); </script>"
    return HttpResponse(msg)

#———————————————————————————————————————— fin
