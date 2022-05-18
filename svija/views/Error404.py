#———————————————————————————————————————— Error404.py

#———————————————————————————————————————— notes
#
#   https://websiteadvantage.com.au/404-Error-Handler-Checker
#
#   Links folder redirection breaks if the prefix does not exist
#   instead of defaulting to en, need to get site default language
#
#   return HttpResponse("debugging message.")
#
# from django.http import HttpResponse
# return HttpResponse("debugging message.")
#
#———————————————————————————————————————— imports

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from modules.cached_page import *
from modules.default_screen_code import *
from svija.models import Redirect, Language, Settings

#———————————————————————————————————————— Error404(request, *args, **kwargs):

#@never_cache # we'll see if this is a problem
def Error404(request, *args, **kwargs):

  image_m = '<pre>\n\n   missing image'
  broken  = '<pre>\n\n   Configuration Error\n\n   Please contact support@svija.com.'
  missing = '<pre>\n\n   Page Missing\n\n   To customize this message, add a page called "missing".'

#———————————————————————————————————————— cases
#
#   page is definitely missing, all we can do is:
#   - send the missing page
#   - print a text message if the missing page is broken
#   
#   BUT, it would be better to
#   - send a 404 page for the correct language
#   - send a 404 page for the correct screen code
#   - send someting small if the missing element is an image
#
#———————————————————————————————————————— possible URL's
#
#   /fr/accueilx/cp
#   /fr/accueilx
#   /fr
#   /accueilx
#   /Links/lmkjs
#   /images/lkjmlkj
#
#   if we split it by slash:
#   - the first part may be a language code
#   - the last part may be a screen code
#
#———————————————————————————————————————— setup

  missing_page_exists = False

#———————————————————————————————————————— check if image

  pf = '.+\.(jpeg|jpg|png|gif)$'

  if re.search(pf, request.path):
      response             = HttpResponse(image_m)
      response.status_code = 404
      return response

#———————————————————————————————————————— get potential screen & language codes

  screen_code = ''
  lang_code   = ''
  parts       = request.path[1:].split('/')

  if len(parts) > 1:
    screen_code = parts[-1]

  if len(parts) > 2:
    lang_code = parts[0]

#———————————————————————————————————————— see if lang_code matches DB

  try:
    # codes correspond
    language = Language.objects.get(code=lang_code)
  except:
    try:
      # codes don't correspond, so use default
      language  = Settings.objects.get(active=True).language
      lang_code = language.code
    except:
      # site settings are broken
      response             = HttpResponse(broken)
      response.status_code = 404
      return response

#———————————————————————————————————————— see if screen code matches DB

  try:
    # codes correspond
    screen  = Screen.objects.get(code=screen_code)
  except:
    try:
      # codes don't correspond, so get default
      screen_code = 'mb'
      screen      = Screen.objects.get(code=screen_code)
    except:
      response             = HttpResponse(broken)
      response.status_code = 404
      return response

#———————————————————————————————————————— have valid screen & language; get "missing" page

  try:
    response = cached_page(request, lang_code, 'missing', screen_code)

  except:
    response = HttpResponse(missing)

  response.status_code = 404
  return response


#———————————————————————————————————————— fin
