
#:::::::::::::::::::::::::::::::::::::::: PageView.py
#
#———————————————————————————————————————— notes
#
#   we assume that the address is correct
#   don't worry about redirects,
#   they're handled after caching
#
#   NOTE: /fr will not go to french home page, because the assumption is that /fr is a page
#   this may not be an actual problem, it just means that links will go to /fr/accueil
#
#   all we need is to supply missing parts
#
#   return HttpResponse("debugging message.")
#
#   from django.http import HttpResponse
#   return HttpResponse("debugging message.")
#
#———————————————————————————————————————— imports

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from svija.models import Section, Settings, Screen

from PageObject import *
from modules.cache_per_user import *
from modules.construct_page import *


def PageView(request, request_sect='', request_page=''):

#———————————————————————————————————————— determine section

  sections = Section.objects.filter(Q(code=request_sect))

  if len(sections) > 0:
    section     = sections.get(code=request_sect)
    section_url = request_sect

  else:
    section     = get_object_or_404(Settings, enabled=True).section
    section_url = section.code

    if request_page == '':
      request_page = request_sect

#———————————————————————————————————————— determine page

  if request_page != '':
    page_url = request_page
  else:
    page_url = section.default_page

#———————————————————————————————————————— get screen code

  screen_code = request.COOKIES.get('screen_code')

  if screen_code is None:
    screen_code = 'xkcd'

  screens = Screen.objects.filter(Q(code=screen_code))

  if len(screens) == 0:
    screen_code = derived_screen(request.headers["User-Agent"])

  request.screen_code = screen_code


  return construct_page(request, section_url, page_url, screen_code, 200)

#:::::::::::::::::::::::::::::::::::::::: functions

#———————————————————————————————————————— derived_screen(user_agent)
#
#   returns mb or cp screen code for known entites
#   returns mb if no info

certain_mb  = [ 'nexus',
                'pixel',
                'android',
                'iphone',
                'mobile',   ]

certain_cp  = [ 'x86_64',
                'intel',
                'windows nt',
                'macintosh',
                'googlebot', ]

def derived_screen(user_agent):

  all_screens = Screen.objects.all().order_by('pixels')

  if len(all_screens) == 1:
    return all_screens[0].code

  screen_cp = all_screens[0].code
  screen_mb = all_screens[1].code

  user_agent = user_agent.lower()

  for str in certain_mb:
    if str in user_agent:
      return screen_mb

  for str in certain_cp:
    if str in user_agent:
      return screen_cp

  return screen_mb


#:::::::::::::::::::::::::::::::::::::::: fin

