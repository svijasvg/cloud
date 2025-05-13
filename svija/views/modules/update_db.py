
#:::::::::::::::::::::::::::::::::::::::: update_db.py
#
#   will check and add data as necessary for various
#   improvements

#———————————————————————————————————————— import

from svija.models import Screen, Section
from django.db.models import Q

#:::::::::::::::::::::::::::::::::::::::: get_accessibility(content):

def update_db():

#———————————————————————————————————————— 2.3.3

#  add * screen if not present

  screens = Screen.objects.filter(Q(code='*'))

  if len(screens) == 0:
    screens = Screen.objects.all()
    return 'no catch-all screen'
    return str(len(screens))

#  add * section if not present

#———————————————————————————————————————— exit

  return False

#:::::::::::::::::::::::::::::::::::::::: fin

# screens = Screen.objects.filter(Q(code=screen_code)).exclude(code='*')
#   screen_code = derived_screen(request.headers["User-Agent"])
