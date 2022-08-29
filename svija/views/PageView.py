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
from modules.cached_page import *

#———————————————————————————————————————— definition

def PageView(request, request_page='', request_lang=''):

#———————————————————————————————————————— lang is missing (one-part page address)

  if request_lang == '':

    # check if page corresponds to section
    # settings = Settings.objects.get(active=True)
    # Font.objects.filter(Q(active=True) & Q(google=True ))

    sections = Section.objects.filter(Q(code=request_page))
    if len(sections) > 0:
      section = sections[0]
      request_lang = request_page
      request_page = ''
      # return HttpResponse("debugging message: " + sections[0].name)
    else:
      # return HttpResponse("not a section")

      section = get_object_or_404(Settings, active=True).section
      request_lang = section.code

#———————————————————————————————————————— page is missing

  # happens for the home page or section home

  if request_page == '':
    request_page = section.default_page

#———————————————————————————————————————— get screen code

  screen_code = request.COOKIES.get('screen_code')

  if str(screen_code) == 'None':
    screen_code = Screen.objects.first().code

  request.screen_code = screen_code

#———————————————————————————————————————— return cached results

  return cached_page(request, request_lang, request_page, screen_code)


#———————————————————————————————————————— fin
