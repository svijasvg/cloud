#———————————————————————————————————————— HomePageView.py
#
#   accepts request.path / or /en
#
#   returns request for /en/home
#
#———————————————————————————————————————— imports

#rom django.http import HttpResponse
from django.shortcuts import get_object_or_404
from svija.models import Language, Settings
from svija.views import PageView
from modules.cache_per_user import *

#———————————————————————————————————————— definition

def HomePageView(request, language_code):
# return HttpResponse('HomePageView: '+request.path +', '+language_code)

#———————————————————————————————————————— get default language for site

  if language_code == '':
    settings = get_object_or_404(Settings, active=True)
    language_code = settings.language.code

#———————————————————————————————————————— get default page for language

  language = get_object_or_404(Language, code=language_code)
  default_page = language.default

#———————————————————————————————————————— return regular view

  return PageView(request, language_code, default_page)

#———————————————————————————————————————— fin
