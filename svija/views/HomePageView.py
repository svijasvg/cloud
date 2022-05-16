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

def HomePageView(request, page_name):

  return HttpResponse("HomePageView.py")
#   root: path: /, page_name: 
#    /en: path: /en/, page_name: en
#   same for other words instead of /en

#———————————————————————————————————————— get default language for site

  settings = get_object_or_404(Settings, active=True)

  # no path after hostname
  if page_name == '':
    language_code = settings.language.code
    page_name = settings.language.default_page

  # one word after hostname
  else:

    # if path is a language code
    language = Language.objects.filter(code=page_name).first()
    if type(language) != type(None):
      language_code = page_name
      page_name = language.default_page

    # if path is not a language code
    else:
      language_code = settings.language.code 

#———————————————————————————————————————— return regular view

  return PageView(request, language_code, page_name)

#———————————————————————————————————————— fin
