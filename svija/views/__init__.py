#———————————————————————————————————————— __init__.py

version = '2.2.28'
import os, sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), './'))
if not path in sys.path: sys.path.insert(1, path)

#SITE_ROOT = os.path.realpath(os.path.dirname(__file__)+'/../')

#———————————————————————————————————————— all views

from .PageObject     import *
from .PageView       import *

from .MailView       import *
from .ClearCacheView import *
from .SendView       import *
from .LinksView      import *
from .RobotsView     import *
from .SitemapView    import *
from .Error404       import *

#———————————————————————————————————————— fin
