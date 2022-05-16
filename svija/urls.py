#———————————————————————————————————————— urls.py

#———————————————————————————————————————— imports

from . import views
from django.urls import path, re_path
from django.views import static
#rom django.views.generic import RedirectView
#rom django.views.decorators.cache import cache_page
import os

#———————————————————————————————————————— variables

proj_folder = os.path.abspath(os.path.dirname(__name__))

app_name = 'svija'
rp = '[A-Za-z0-9À-ÖØ-öø-ÿ_ \.\/-]*links'
pf = '[A-Za-z0-9À-ÖØ-öø-ÿ_ \.-]+\.(jpeg|jpg|png|gif)'

#———————————————————————————————————————— ▼ url patterns

urlpatterns = [ 

#———————————————————————————————————————— exact addresses

    path('csync',       views.ClearCacheView),   # Sync + Admin top bar
    path('mail',        views.MailView      ),
    path('send',        views.SendView      ),   # send test mail to see what happens
    path('robots.txt',  views.RobotsView    ),
    path('sitemap.txt', views.SitemapView   ),

#———————————————————————————————————————— images in Links folder

#   replaced \w with A-Za-z0-9À-ÖØ-öø-ÿ to permit accented filenames & folders
#   https://stackoverflow.com/questions/56279948/remove-special-characters-but-not-accented-letters

    re_path(r'^(?P<request_prefix>' + rp + ')/(?P<placed_file>' + pf + ')$(?i)', views.LinksView),

#———————————————————————————————————————— SVG pages

    path('',                                        views.PageView),   # prefix/slug
    path('<slug:request_page>',                     views.PageView),   # prefix/slug
    path('<slug:request_lang>/<slug:request_page>', views.PageView),   # prefix/slug

#———————————————————————————————————————— fonts, icons & scripts

    re_path(r'^customization/(?P<path>.*)$(?i)', static.serve, {'document_root': proj_folder + "/sync/Svija/Svija Admin"      }),
    re_path(r'^fonts/(?P<path>.*)$(?i)',         static.serve, {'document_root': proj_folder + "/sync/Svija/Fonts/WOFF Files" }),
    re_path(r'^files/(?P<path>.*)$(?i)',         static.serve, {'document_root': proj_folder + "/sync/Svija/Shared Files"     }),
    re_path(r'^images/(?P<path>.*)$(?i)',        static.serve, {'document_root': proj_folder + "/sync/Svija/Images"           }),


]

#———————————————————————————————————————— unused but still in code

#   path('lab', views.LabView),


#———————————————————————————————————————— fin
