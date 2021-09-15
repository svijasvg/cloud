#———————————————————————————————————————— HomePageView.py

#———————————————————————————————————————— imports

from django.shortcuts import get_object_or_404
from svija.models import Language, Settings
from svija.views import SubPageView
from modules.cache_per_user import *

#———————————————————————————————————————— definition

def HomePageView(request, language_code):

  screen = request.COOKIES.get('screen')
  if (screen == None): 
    # calculate minimum screen
    screen = 'mb'

#———————————————————————————————————————— different from regular page

  if language_code == '':
    settings = get_object_or_404(Settings, active=True)
    language_code = settings.language.code

  language = get_object_or_404(Language, code=language_code)
  request_slug = language.default

#———————————————————————————————————————— same as regular page

  return SubPageView(request, language_code, request_slug, screen)

#———————————————————————————————————————— fin
