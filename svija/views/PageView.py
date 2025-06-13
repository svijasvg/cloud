
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
#   urls.py
#   path('',                                   views.PageView),   # prefix/slug
#   path('<slug:section_url>',                 views.PageView),   # prefix/slug
#   path('<slug:section_url>/<slug:page_url>', views.PageView),   # prefix/slug
#
#———————————————————————————————————————— imports

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from svija.models import Section, Settings, Screen

from PageObject import *
from modules.cache_per_user import *
from modules.construct_page import *


def PageView(request, section_url='', page_url=''):

#———————————————————————————————————————— if /page, correct section_url
#                                         and _page_url

  if page_url == '' and section_url != '' :
    sections = Section.objects.filter(Q(code=section_url) & Q(enabled=True))

    if len(sections) == 0:
      page_url    = section_url
      section_url = ''

#———————————————————————————————————————— if section = '' get default

  if section_url == '':
    section     = get_object_or_404(Settings, enabled=True).section
    section_url = section.code

#———————————————————————————————————————— get section or 404

  section = get_object_or_404(Section, code=section_url, enabled=True)

#———————————————————————————————————————— if page_url = '' get default

  if page_url == '':
    page_url = get_object_or_404(Section, code=section_url).default_page

#———————————————————————————————————————— get screen code

  screen_code = request.COOKIES.get('screen_code')

  if screen_code is None:
    screen_code = 'xkcd'

  screens = Screen.objects.filter(Q(code=screen_code)).exclude(code='*')

  if len(screens) == 0:
    screen_code = derived_screen(request.headers["User-Agent"])

  request.screen_code = screen_code # needed by cache_per_user.py


# return HttpResponse("<pre>"+str(screen_code))

  return construct_page(request, section_url, page_url, screen_code, 200) # why code 200?

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

  all_screens = Screen.objects.all().exclude(code='*').order_by('pixels')

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

