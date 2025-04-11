#———————————————————————————————————————— ClearCacheView.py
#
# Header set Access-Control-Allow-Origin
#
# /csync clears cache, for admins only, launched by Svija Sync
# or by header in admin pages
# returns 1 in case of success

from django.core.cache import cache as memcache
from django.http import HttpResponse
from svija.views import PageView

def ClearCacheView(request):

#   if not request.user.is_superuser:
#       response = PageView(request, 'en','missing',)
#       response.status_code = 404
#       return response

    memcache.clear()
    return HttpResponse(1)

#———————————————————————————————————————— fin
