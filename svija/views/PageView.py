#———————————————————————————————————————— PageView.py
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
# from django.http import HttpResponse
# return HttpResponse("debugging message.")
#
#———————————————————————————————————————— imports

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from svija.models import Section, Settings, Screen

from PageObject import *
from modules.cache_per_user import *
from modules.construct_page import *

#———————————————————————————————————————— definition

def PageView(request, request_page='', request_lang=''):
# return HttpResponse("debugging message.")

#———————————————————————————————————————— lang is missing (one-part page address)

  if request_lang == '':

    # check if page corresponds to section
    # settings = Settings.objects.get(enabled=True)
    # Font.objects.filter(Q(enabled=True) & Q(google=True ))

    sections = Section.objects.filter(Q(code=request_page))
    if len(sections) > 0:
      section = sections[0]
      request_lang = request_page
      request_page = ''
      # return HttpResponse("debugging message: " + sections[0].name)
    else:
      # return HttpResponse("not a section")

      section = get_object_or_404(Settings, enabled=True).section
      request_lang = section.code

#———————————————————————————————————————— page is missing

  # happens for the home page or section home

  if request_page == '':
    request_page = section.default_page

#———————————————————————————————————————— get screen code

  screen_code = request.COOKIES.get('screen_code')
  all_screens   = Screen.objects.all().order_by('pixels')

#———————————————————————————————————————— check if valid

  have_valid_code = False

  if str(screen_code) != 'None':
    for screen in all_screens:
      if screen_code == screen.code:
        have_valid_code = True

#———————————————————————————————————————— get screen code

  if not have_valid_code:

    if all_screens[0].pixels == 0 and len(all_screens) > 1:
      screen_code = all_screens[1].code
    else:
      screen_code = all_screens[0].code

  request.screen_code = screen_code

#———————————————————————————————————————— return cached results

  return construct_page(request, request_lang, request_page, screen_code)


#———————————————————————————————————————— fin
