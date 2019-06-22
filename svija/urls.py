from . import views

from django.urls import path, re_path

from django.views import static
from django.views.generic import RedirectView
from django.views.decorators.cache import cache_page

#https://stackoverflow.com/questions/17820980/how-can-i-load-a-static-font-file-for-use-with-pil-in-django
import os
#ITE_ROOT = os.path.realpath(os.path.dirname(__file__)+'/../')
SITE_ROOT = os.path.abspath(os.path.dirname(__name__))
    #source_dir = os.path.abspath(os.path.dirname(__file__)+'/../') + '/' + source_dir

app_name = 'svija'

urlpatterns = [ 
#---------------------------------------- default url's

    re_path(r'^(?P<path1>)$', views.HomePage),
    re_path(r'^(?P<path1>[\w-]{2})/$', views.HomePage),

#---------------------------------------- email sending

    path('<slug:lng>/mail', views.MailView),

#---------------------------------------- placed images (in Links folder)

    re_path(r'^(?P<path1>[\w-]+)/Links/(?P<placed_file>[\w-]+\.(jpeg|jpg|png|gif|JPEG|JPG|PNG|GIF))$', views.LinksView),

    # special case of home page which has no /en/
    re_path(r'^Links/(?P<placed_file>[\w-]+\.(jpeg|jpg|png|gif|JPEG|JPG|PNG|GIF))$', views.LinksViewHome),

#---------------------------------------- txt views

    path('robots.txt', views.RobotsView),
    path('sitemap.txt', views.SitemapView),

#---------------------------------------- fonts, images & scripts
# source_dir = responsive.source_dir

    re_path(r'^fonts/(?P<path>.*)$', static.serve, {'document_root': SITE_ROOT + "/sync/fonts"}),
    re_path(r'^images/(?P<path>.*)$', static.serve, {'document_root': SITE_ROOT + "/sync/images"}),
    re_path(r'^scripts/(?P<path>.*)$', static.serve, {'document_root': SITE_ROOT + "/scripts"}),

#---------------------------------------- main page view

# https://docs.djangoproject.com/en/2.2/topics/cache/#the-per-view-cache
# first need to change to per-view caching

#   if request.GET.get('clear') == 'cache':
#       if request.user.is_superuser:
#           title = request.GET.get('flag') + ' - ' + title 
#           cache.clear()

    #path('<slug:path1>/<slug:path2>', views.PageView),
    path('<slug:path1>/<slug:path2>', cache_page(60 * 15)(views.PageView)),

]

# this whole idea can never work because urls.py is loaded first
# instead, use a wrapper for the page view that checks the user
# status then caches. Oops, that won't work because the view
# will be cached, will never run the test.

#if lambda request: request.user.is_superuser:
#if request.user.is_superuser:
#    del urlpatterns[-1]
#    urlpatterns.append(path('<slug:path1>/<slug:path2>', views.PageView),)

#---------------------------------------- 404 page

# project urls.py that this happens
# handler404 = 'views.error404'

#---------------------------------------- fin
