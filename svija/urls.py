#———————————————————————————————————————— urls.py

#———————————————————————————————————————— imports

from . import views
from django.urls import path, re_path
from django.views import static
from django.views.generic import RedirectView
from django.views.decorators.cache import cache_page
import os

#———————————————————————————————————————— variables

proj_folder = os.path.abspath(os.path.dirname(__name__))

app_name = 'svija'
rp = '[A-Za-z0-9À-ÖØ-öø-ÿ \.\/-]*links'
pf = '[A-Za-z0-9À-ÖØ-öø-ÿ \.-]+\.(jpeg|jpg|png|gif)'


urlpatterns = [ 

#———————————————————————————————————————— exact addresses

    path('c', views.ClearCacheView),
    path('csync', views.ClearCacheSyncView),

#———————————————————————————————————————— email sending

    # used by contact page
    path('<slug:lng>/mail', views.MailView),

    # send test mail to see what happens
    path('<slug:lng>/send', views.SendView),

#———————————————————————————————————————— placed images (in Links folder)

#   replaced \w with A-Za-z0-9À-ÖØ-öø-ÿ to permit accented filenames & folders
#   https://stackoverflow.com/questions/56279948/remove-special-characters-but-not-accented-letters

    re_path(r'^(?P<request_prefix>' + rp + ')/(?P<placed_file>' + pf + ')$(?i)', views.LinksView),

#———————————————————————————————————————— home pages

    re_path(r'^(?P<request_prefix>)$', views.HomePageView),          # root url
    re_path(r'^(?P<request_prefix>[\w-]{2})/$', views.HomePageView), # two letters followed by slash

#———————————————————————————————————————— regular pages

    path('<slug:request_prefix>/<slug:request_slug>', views.PageView),  # prefix/slug

#———————————————————————————————————————— txt views

    path('lab', views.LabView),
    path('robots.txt', views.RobotsView),
    path('sitemap.txt', views.SitemapView),

#———————————————————————————————————————— fonts, icons & scripts

    re_path(r'^admn/(?P<path>.*)$(?i)',    static.serve, {'document_root': proj_folder + "/sync/Svija/Admin Customization"}),
    re_path(r'^fonts/(?P<path>.*)$(?i)',   static.serve, {'document_root': proj_folder + "/sync/Svija/Fonts/WOFF Files"   }),
    re_path(r'^files/(?P<path>.*)$(?i)',   static.serve, {'document_root': proj_folder + "/sync/Svija/Shared Files"       }),
    re_path(r'^images/(?P<path>.*)$(?i)',  static.serve, {'document_root': proj_folder + "/sync/Svija/Icons"              }),
    re_path(r'^scripts/(?P<path>.*)$(?i)', static.serve, {'document_root': proj_folder + "/sync/Svija/Site Scripts"       }),


]

#———————————————————————————————————————— fin
