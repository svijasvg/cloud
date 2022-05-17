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
#———————————————————————————————————————— imports

#rom django.http import HttpResponse
from django.shortcuts import get_object_or_404
from svija.models import Language, Settings
from modules.default_screen_code import *

from PageObject import *
from modules.cache_per_user import *
from modules.cached_page import *

#———————————————————————————————————————— definition

def PageView(request, request_page='', request_lang=''):

#———————————————————————————————————————— lang is missing

  if request_lang == '':
    language = get_object_or_404(Settings, active=True).language
    request_lang = language.code

#———————————————————————————————————————— page is missing

  # this only happens for the home page
  # so we have already gotten settings above

  if request_page == '':
    request_page = language.default_page

#———————————————————————————————————————— get screen code

  screen_code = request.COOKIES.get('screen_code')
  if screen_code == None:
    screen_code = default_screen_code(request)

#———————————————————————————————————————— status

#   at this point we have language/page/screencode
#   can make request for cached content

#———————————————————————————————————————— return cached results

  return cached_page(request, request_lang, request_page, screen_code)


#———————————————————————————————————————— fin
