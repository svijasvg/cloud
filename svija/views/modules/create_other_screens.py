
#:::::::::::::::::::::::::::::::::::::::: create_other_screens.py 

#———————————————————————————————————————— notes
#
#   given a page and a screen code, this method
#   will create versions for other screen codes
#   if they don't exist.
#
#   to do this it is necessary to copy the foreign
#   key models like modules, illustrator files etc.
#
#———————————————————————————————————————— import

from svija.models import Screen, Page
from django.db.models import Q

def create_other_screens(page, screen_code):

  return True

  section_code = page.section.code
  request_slug = page.url

  all_screens = Screen.objects.all()
  for this_screen in all_screens:
    this_code = this_screen.code
    these_screen_pages = Page.objects.filter(Q(section__code=section_code) & Q(screen__code=this_code) & Q(url=request_slug))

    # if there's no page with this code
    if len(these_screen_pages) == 0:

      #https://stackoverflow.com/a/48015925/72958
      a_dict = page.__dict__


















      # THIS THROWS AN ERROR 1/2 OF THE TIME
      del a_dict['_state']
      del a_dict['id']
      new_page = Page.objects.create(**a_dict) 

      new_page.screen = this_screen
      new_page.save()


  return True

#   doesn't copy other models, so no scripts, modules or illustrator files
#:::::::::::::::::::::::::::::::::::::::: fin

