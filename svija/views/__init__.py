#———————————————————————————————————————— __init__.py

import os, sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), './'))
if not path in sys.path: sys.path.insert(1, path)

SITE_ROOT = os.path.realpath(os.path.dirname(__file__)+'/../')

#———————————————————————————————————————— all views

from .LinksView      import *
from .MailView       import *
from .AllViews       import *
from .ClearCacheView import *
from .LabView        import *
from .RobotsView     import *
from .SitemapView    import *

# must be last
from .Error404       import *

#———————————————————————————————————————— fin
