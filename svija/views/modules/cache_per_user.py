#———————————————————————————————————————— views/modules/cache_functions.py

#   https://gist.github.com/caot/6480c39453f5d2fa86bf

#———————————————————————————————————————— imports

from django.core.cache import cache
from django.core.cache import cache as memcache
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from svija.models import Control

#———————————————————————————————————————— original notes
#
#   https://gist.github.com/caot/6480c39453f5d2fa86bf
#   
#   Decorator which caches the view for each User
#   
#   * ttl - the cache lifetime, do not send this parameter means
#     that the cache will last until the restart server or decide to remove it
#   
#   * cache_post - Determine whether to make requests cache POST
#   
#   * The caching for anonymous users is shared with everyone
#   
#   How to use it:
#   @cache_per_user(ttl=3600, cache_post=False)
#   def my_view(request):
#       return HttpResponse("LOL %s" % (request.user))
#
#———————————————————————————————————————— page caching (applied to Page view below)

def cache_per_user(ttl=None, cache_post=False):
    def decorator(function):
        def apply_cache(request, *args, **kwargs):

            CACHE_KEY             = cache_key(request)
            return_cached_content = True
            page_content          = None

#———————————————————————————————————————— no cache if control.cached = false

            # models ending in _h are not visible in admin
            control = Control.objects.first()

            if type(control) is type(None):
              return_cached_content = False
            elif control.password != 'aYtr)54Ytrf':
              control.limit      = control.limit_h
              control.used       = control.used_h
              control.cached     = control.cached_h
              control.password   = ''
              control.save()
              return_cached_content = control.cached_h
            else:
              control.limit_h    = control.limit
              control.used_h     = control.used
              control.cached_h   = control.cached
              control.password   = ''
              control.save()
              return_cached_content = control.cached_h

#———————————————————————————————————————— no cache for POST or admins

            if not cache_post and request.method == 'POST':
              return_cached_content = False

            if request.user.is_superuser:
              return_cached_content = False

#———————————————————————————————————————— cached if necessary


            if return_cached_content:
                page_content = memcache.get(CACHE_KEY, None)

            if page_content is None:
                page_content = function(request, *args, **kwargs)
                if return_cached_content:
                    memcache.set(CACHE_KEY, page_content, ttl)

            return page_content
        return apply_cache
    return decorator

#———————————————————————————————————————— cache_key(request):

def cache_key(request):
    q = getattr(request, request.method)
    q.lists()
    urlencode = q.urlencode(safe='()')

    return 'pageview_%s_%s' % (request.path, urlencode)


#———————————————————————————————————————— fin
