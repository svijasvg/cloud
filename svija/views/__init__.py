#———————————————————————————————————————— __init__.py

version = '2.2.4'
import os, sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), './'))
if not path in sys.path: sys.path.insert(1, path)

#SITE_ROOT = os.path.realpath(os.path.dirname(__file__)+'/../')

#———————————————————————————————————————— all views


#   path('<slug:lng>/mail', views.MailView),
from .MailView       import *

#   path('<slug:path1>/<slug:path2>', views.PageView),  # prefix/slug
from .PageView       import *

#   path('c', views.ClearCacheView), depends on PageView
from .ClearCacheView import *

#   path('csync', views.ClearCacheSyncView),
from .ClearCacheSyncView import *

#   path('<slug:lng>/send', views.SendView), depends on PageView
from .SendView       import *

#   re_path(r'^(?P<path1>)$', views.HomePageView),          # root url
#   re_path(r'^(?P<path1>[\w-]{2})/$', views.HomePageView), # two letters followed by slash
from .HomePageView   import *

#   re_path(r'^(?P<path1>[\w-]+)/links/(?P<placed_file>[\w\-\ \.]+\.(jpeg|jpg|png|gif))$(?i)', views.LinksView),
#   re_path(r'^links/(?P<placed_file>[\w\-\ \.]+\.(jpeg|jpg|png|gif))$(?i)', views.LinksViewHome),
from .LinksView      import *

#   path('lab', views.LabView),
from .LabView        import *

#   path('robots.txt', views.RobotsView),
from .RobotsView     import *

#   path('sitemap.txt', views.SitemapView),
from .SitemapView    import *

# must be last
from .Error404       import *

#———————————————————————————————————————— fin
