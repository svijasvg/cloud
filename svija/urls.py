from django.urls import path, re_path
from . import views
from django.views.generic import RedirectView
from django.views import static
#from svija import settings


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

#---------------------------------------- from tutorial

#   path('<int:pk>/', views.DetailView.as_view(), name='detail'),
#   path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
#   path('<int:page_id>/vote/', views.vote, name='vote'),

#---------------------------------------- email sending

    path('<slug:lng>/mail', views.MailView),

#---------------------------------------- main page view

#   path('<slug:path1>/<slug:path2>', views.PageView),

#---------------------------------------- placed images (in Links folder)

    re_path(r'^(?P<path1>[\w-]+)/Links/(?P<placed_file>[\w-]+\.(jpeg|jpg|png|gif|JPEG|JPG|PNG|GIF))$', views.LinksView),

    # special case of home page which has no /en/
    re_path(r'^Links/(?P<placed_file>[\w-]+\.(jpeg|jpg|png|gif|JPEG|JPG|PNG|GIF))$', views.LinksViewHome),

#---------------------------------------- txt views

    path('robots.txt', views.RobotsView),
    path('sitemap.txt', views.SitemapView),

#---------------------------------------- fonts
# source_dir = responsive.source_dir

    # https://stackoverflow.com/questions/18446922/make-two-directories-static-in-django
    # url(r'^uploads/(?P<path>.*)$', static.serve, {'document_root': settings.BASE_DIR + "/uploads"}),
    re_path(r'^fonts/(?P<path>.*)$', static.serve, {'document_root': SITE_ROOT + "/sync/fonts"}),

#---------------------------------------- images folder

    re_path(r'^images/(?P<path>.*)$', static.serve, {'document_root': SITE_ROOT + "/sync/images"}),

#---------------------------------------- scripts folder

    re_path(r'^scripts/(?P<path>.*)$', static.serve, {'document_root': SITE_ROOT + "/scripts"}),

]
#---------------------------------------- 404 page

# à priori it's in the svija urls.py that this happens
#handler404 = 'views.error404'

#---------------------------------------- fin
