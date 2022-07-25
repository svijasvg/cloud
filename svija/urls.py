#———————————————————————————————————————— urls.py

#———————————————————————————————————————— imports

from . import views
from django.urls import path, re_path
from django.views import static
import os

#———————————————————————————————————————— variables

proj_folder = os.path.abspath(os.path.dirname(__name__))

app_name = 'svija'

# for images in Links folder PREVIOUS
#   image_folder = '[A-Za-z0-9À-ÖØ-öø-ÿ_ \.\/-]*links'
#   image_file = '[A-Za-z0-9À-ÖØ-öø-ÿ_ \.-]+\.(jpeg|jpg|png|gif)'

# "../../Links/shadow drop.png"

image_folder = '.*links'                  # image folder
image_file = '.*\.(jpeg|jpg|png|gif)'   # image file

# https://www.regular-expressions.info/modifiers.html

# (?i) makes regex case insensitive


#:::::::::::::::::::::::::::::::::::::::: url patterns

urlpatterns = [ 

#———————————————————————————————————————— exact addresses

    path('csync',       views.ClearCacheView),   # Sync + Admin top bar
    path('mail',        views.MailView      ),
    path('send',        views.SendView      ),   # send test mail to see what happens
    path('robots.txt',  views.RobotsView    ),
    path('sitemap.txt', views.SitemapView   ),

#———————————————————————————————————————— images in Links folder
#
#   accepts any path ending in links › / › any path ending in .jpg etc.
#
#   at top of this file:
#
#   image_folder = '.*links'                  # image folder
#   image_file = '.*\.(jpeg|jpg|png|gif)'   # image file

    re_path(r'^(?P<request_prefix>' + image_folder + ')/(?P<placed_file>' + image_file + ')$(?i)', views.LinksView),

#———————————————————————————————————————— SVG pages

    path('',                                        views.PageView),   # prefix/slug
    path('<slug:request_page>',                     views.PageView),   # prefix/slug
    path('<slug:request_lang>/<slug:request_page>', views.PageView),   # prefix/slug

#———————————————————————————————————————— redirects

#   redirects are handled by Error404.py
#   that filename is determined by urls.py in the site project folders

#———————————————————————————————————————— fonts, icons & scripts

    re_path(r'^customization/(?P<path>.*)$(?i)', static.serve, {'document_root': proj_folder + "/sync/Svija/Svija Admin"      }),
    re_path(r'^fonts/(?P<path>.*)$(?i)',         static.serve, {'document_root': proj_folder + "/sync/Svija/Fonts/WOFF Files" }),
    re_path(r'^files/(?P<path>.*)$(?i)',         static.serve, {'document_root': proj_folder + "/sync/Svija/Shared Files"     }),
    re_path(r'^images/(?P<path>.*)$(?i)',        static.serve, {'document_root': proj_folder + "/sync/Svija/Images"           }),


]

#———————————————————————————————————————— fin
