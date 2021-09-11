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
#———————————————————————————————————————— exact addresses

    path('c', views.ClearCacheView),
    path('csync', views.ClearCacheSyncView),

#———————————————————————————————————————— email sending

    path('<slug:lng>/mail', views.MailView),
    path('<slug:lng>/send', views.SendView),

#———————————————————————————————————————— home pages

    re_path(r'^(?P<request_prefix>)$', views.HomePageView),          # root url
    re_path(r'^(?P<request_prefix>[\w-]{2})/$', views.HomePageView), # two letters followed by slash

#———————————————————————————————————————— regular pages

    path('<slug:request_prefix>/<slug:request_slug>', views.PageView),  # prefix/slug

#———————————————————————————————————————— placed images (in Links folder)
# xlink:href="links/image.jpg", in page at /fr/contact

    re_path(r'^(?P<request_prefix>[\w-]+)/links/(?P<placed_file>[\w\-\ \.]+\.(jpeg|jpg|png|gif))$(?i)', views.LinksView),

    # special case: home page, has no /en/
    re_path(r'^links/(?P<placed_file>[\w\-\ \.]+\.(jpeg|jpg|png|gif))$(?i)', views.LinksViewHome),

#———————————————————————————————————————— txt views

    path('lab', views.LabView),
    path('robots.txt', views.RobotsView),
    path('sitemap.txt', views.SitemapView),

#———————————————————————————————————————— fonts, images & scripts
# source_dir = responsive.source_dir

    re_path(r'^admn/(?P<path>.*)$(?i)', static.serve, {'document_root': SITE_ROOT + "/sync/Svija/Admin Customization"}),
    re_path(r'^fonts/(?P<path>.*)$(?i)', static.serve, {'document_root': SITE_ROOT + "/sync/Svija/Fonts/WOFF Files"}),
    re_path(r'^files/(?P<path>.*)$(?i)', static.serve, {'document_root': SITE_ROOT + "/sync/Svija/shared files"}),
    re_path(r'^images/(?P<path>.*)$(?i)', static.serve, {'document_root': SITE_ROOT + "/sync/Svija/Icons"}),
    re_path(r'^scripts/(?P<path>.*)$(?i)', static.serve, {'document_root': SITE_ROOT + "/sync/Svija/Site Scripts"}),

]

#———————————————————————————————————————— fin


