#———————————————————————————————————————— ClearCacheView.py
# /c clears cache, for admins only

from django.core.cache import cache as memcache
from django.http import HttpResponse

def ClearCacheView(request):
    if request.user.is_superuser:
        memcache.clear()
        return HttpResponse('<pre>Cache cleared.')
    else:
        response = PageView(request, '', 'missing',)
        response.status_code = 404
        return response

#———————————————————————————————————————— fin
