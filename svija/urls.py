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
#---------------------------------------- email sending

    path('<slug:lng>/mail', views.MailView),

#---------------------------------------- main pages

    re_path(r'^(?P<path1>)$', views.HomePage),                # root url
    re_path(r'^(?P<path1>[\w-]{2})/$', views.HomePage),       # two letters followed by slash
    path('<slug:path1>/<slug:path2>', views.PageView),  # something/something

#---------------------------------------- placed images (in Links folder)
# xlink:href="links/image.jpg"

#   re_path(r'(?i)^(?P<path1>[\w-]+)/Links/(?P<placed_file>[\w\-\ ]+\.(jpeg|jpg|png|gif|JPEG|JPG|PNG|GIF))$', views.LinksView),
    re_path(r'^(?P<path1>[\w-]+)/links/(?P<placed_file>[\w\-\ \.]+\.(jpeg|jpg|png|gif))$(?i)', views.LinksView),

    # special case of home page which has no /en/
#   re_path(r'(?i)^Links/(?P<placed_file>[\w\-\ ]+\.(jpeg|jpg|png|gif|JPEG|JPG|PNG|GIF))$', views.LinksViewHome),
    re_path(r'^links/(?P<placed_file>[\w\-\ \.]+\.(jpeg|jpg|png|gif))$(?i)', views.LinksViewHome),

#---------------------------------------- txt views

    path('lab', views.LabView),
    path('robots.txt', views.RobotsView),
    path('sitemap.txt', views.SitemapView),

#---------------------------------------- fonts, images & scripts
# source_dir = responsive.source_dir

    re_path(r'^fonts/(?P<path>.*)$', static.serve, {'document_root': SITE_ROOT + "/sync/fonts"}),
    re_path(r'^images/(?P<path>.*)$', static.serve, {'document_root': SITE_ROOT + "/sync/images"}),
    re_path(r'^scripts/(?P<path>.*)$', static.serve, {'document_root': SITE_ROOT + "/scripts"}),

]

#---------------------------------------- fin
