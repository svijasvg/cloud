#———————————————————————————————————————— HomePageView.py
#
#   accepts request.path / or /en
#
#   returns request for /en/home
#
#   return HttpResponse("debugging message.")
#
#———————————————————————————————————————— imports

#rom django.http import HttpResponse
from django.shortcuts import get_object_or_404
from svija.models import Language, Settings
from svija.views import PageView
from modules.cache_per_user import *

#———————————————————————————————————————— definition

def HomePageView(request, language_code):

  return HttpResponse("<pre>path: "+request.path +', language_code: '+language_code)

#   root: path: /, language_code: 
#    /en: path: /en/, language_code: en
#   same for other words instead of /en

#———————————————————————————————————————— get default language for site

  # it's the home page
  if language_code == '':
    settings = get_object_or_404(Settings, active=True)
    language_code = settings.language.code

  # this should be the same thing, non?
  elif request.path != '/':
    language = get_object_or_404(Language, code=language_code)
    default_page = language.default_page




#———————————————————————————————————————— return regular view

  return HttpResponse("debugging: " + language_code + ':' + request.path);
  return PageView(request, language_code, default_page)

#———————————————————————————————————————— fin
