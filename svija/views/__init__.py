#———————————————————————————————————————— robots.txt


#def RobotsView(request):
#    settings = get_object_or_404(Settings,active=True)
#    response = settings.robots.contents
#    return HttpResponse(response, content_type='text/plain; charset=utf8')

from .LinksView import *
from .AllViews import *
from .ClearCacheView import *
from .LabView import *
from .RobotsView import *
from .SitemapView import *

#———————————————————————————————————————— sitemap.txt
