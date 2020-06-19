#———————————————————————————————————————— views/modules/cache_functions.py

#———————————————————————————————————————— page caching (applied to Page view below)
# https://gist.github.com/caot/6480c39453f5d2fa86bf

from django.core.cache import cache
from django.core.cache import cache as memcache
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404
from svija.models import Settings, Page, Module

def cache_key(request):
    q = getattr(request, request.method)
    q.lists()
    urlencode = q.urlencode(safe='()')

    return 'pageview_%s_%s' % (request.path, urlencode)

'''
https://gist.github.com/caot/6480c39453f5d2fa86bf

Decorator which caches the view for each User
* ttl - the cache lifetime, do not send this parameter means that the cache will last until the restart server or decide to remove it
* cache_post - Determine whether to make requests cache POST
* The caching for anonymous users is shared with everyone

How to use it:
@cache_per_user(ttl=3600, cache_post=False)
def my_view(request):
    return HttpResponse("LOL %s" % (request.user))
'''

def cache_per_user(ttl=None, cache_post=False):
    def decorator(function):
        def apply_cache(request, *args, **kwargs):
            CACHE_KEY = cache_key(request)
            return_cached_content = True
            page_content = None

            if not cache_post and request.method == 'POST':
                return_cached_content = False

            if request.user.is_superuser:
                return_cached_content = False

            #  admins see cached content?
            settings = get_object_or_404(Settings,active=True)

            pages = Page.objects.filter(cache_reset=True)
            page_count = Page.objects.filter(cache_reset=True).count()

            modules = Module.objects.filter(cache_reset=True)
            module_count = Module.objects.filter(cache_reset=True).count()

            if reset_cache_flag(pages, modules, page_count, module_count):
                memcache.clear()
                return_cached_content = False
            elif settings.cached: # cached even for superusers
                return_cached_content = True

            if return_cached_content:
                page_content = memcache.get(CACHE_KEY, None)

            if not page_content:
                page_content = function(request, *args, **kwargs)
                if return_cached_content:
                    memcache.set(CACHE_KEY, page_content, ttl)

            return page_content
        return apply_cache
    return decorator


#———————————————————————————————————————— check if cache should be reset

def reset_cache_flag(pages, modules, page_count, module_count):

    if (page_count > 0):
        for this_page in pages:
           this_page.cache_reset = False
           this_page.save()

    if (module_count > 0):
        for this_module in modules:
           this_module.cache_reset = False
           this_module.save()

    if (page_count > 0 or module_count > 0):
        return True
    else:
        return False

