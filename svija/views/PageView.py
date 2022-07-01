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
from svija.models import Language, Settings
from modules.default_screen_code import *

from PageObject import *
from modules.cache_per_user import *
from modules.cached_page import *

#———————————————————————————————————————— definition

def PageView(request, request_page='', request_lang=''):

#———————————————————————————————————————— lang is missing (one-part page address)

  if request_lang == '':

    # check if page corresponds to language
    # settings = Settings.objects.get(active=True)
    # Font.objects.filter(Q(active=True) & Q(google=True ))

    languages = Language.objects.filter(Q(code=request_page))
    if len(languages) > 0:
      language = languages[0]
      request_lang = request_page
      request_page = ''
      # return HttpResponse("debugging message: " + languages[0].name)
    else:
      # return HttpResponse("not a language")

      language = get_object_or_404(Settings, active=True).language
      request_lang = language.code

#———————————————————————————————————————— page is missing

  # happens for the home page or language home

  if request_page == '':
    request_page = language.default_page

#———————————————————————————————————————— get screen code

  screen_code = request.COOKIES.get('screen_code')
  if screen_code == None:
    screen_code = default_screen_code(request)

#———————————————————————————————————————— add screen code to path for cache

  request.path += '/' + screen_code

#———————————————————————————————————————— return cached results

  return cached_page(request, request_lang, request_page, screen_code)


#———————————————————————————————————————— fin
