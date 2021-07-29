#———————————————————————————————————————— ClearCacheSyncView.py
#
# /csync clears cache, for admins only, launched by Svija Sync
# same as ClearCacheView except for response

from django.core.cache import cache as memcache
from django.http import HttpResponse
from svija.views import PageView

def ClearCacheSyncView(request):
#   if not request.user.is_superuser:
#       response = PageView(request, 'en','missing',)
#       response.status_code = 404
#       return response

    memcache.clear()
    return HttpResponse(1)

#———————————————————————————————————————— fin
