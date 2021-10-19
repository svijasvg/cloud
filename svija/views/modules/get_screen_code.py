#———————————————————————————————————————— get_screen_code.py

#———————————————————————————————————————— definition

from svija.models import Responsive 

def get_screen_code(request):

  code = request.COOKIES.get('screen_code')
  if code != None: return code 

#———————————————————————————————————————— get smallest resolution screen code

  all_screens = Responsive.objects.order_by('limit')

  if (len(all_screens) == 1):
    code = all_screens[0].code
  else:
    code = all_screens[1].code

  return code


#———————————————————————————————————————— fin
