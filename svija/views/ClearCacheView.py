#———————————————————————————————————————— ClearCacheView.py
# /c clears cache, for admins only

from django.core.cache import cache as memcache
from django.http import HttpResponse

def ClearCacheView(request):
    if request.user.is_superuser:
        memcache.clear()
        msg = "<html><body><script> alert('Cache deleted.'); window.history.go(-1); </script>"
        return HttpResponse(msg)
    else:
        response = PageView(request, '', 'missing',)
        response.status_code = 404
        return response

#———————————————————————————————————————— fin
