#———————————————————————————————————————— default_screen_code.py

#———————————————————————————————————————— definition

from svija.models import Screen 

def default_screen_code(request):

  all_screens = Screen.objects.order_by('pixels')

  if (len(all_screens) == 1):
    code = all_screens[0].code
  else:
    code = all_screens[1].code

  return code


#———————————————————————————————————————— fin
