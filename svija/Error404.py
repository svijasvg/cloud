#———————————————————————————————————————— Error404.py

# this should be renamed Error404.py

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

  missing_page = 'missing'
  missing_msg = '<pre>\n\n   Page Missing\n\n   To customize this message, add a page called "' + missing_page + '".'

#———————————————————————————————————————— redirect

  try:
    redirect_obj = Redirect.objects.get(from_url=request.path, active=True)
    return HttpResponsePermanentRedirect(redirect_obj.to_url)
  except ObjectDoesNotExist: pass


#:::::::::::::::::::::::::::::::::::::::: actual 404 error

#   the page is missing, but we can accelerate the process by sending the correct screen code
#   the page is missing, but we can be nice and send the missing page for the correct language

#———————————————————————————————————————— language if specified

  request_path_code = 'none'

  if '/' in request_path:
    request_path_code = request.path.split('/')[1]
  
  try:
    language_code = Language.objects.get(code=request_path_code).code
  except:
    try:
      settings = Settings.objects.get(active=True)
      language_code = settings.language.code
    except:
      response = HttpResponse(missing_msg)
      response.status_code = 404
      return response

#———————————————————————————————————————— get screen if possible

  screen_code = default_screen_code(request)

#———————————————————————————————————————— return correct missing page

  try:
    response = cached_page(request, language_code, missing_page, screen_code)

  except:
    response = HttpResponse(missing_msg)
    #esponse = HttpResponse(request.path)

  response.status_code = 404
  return response


#———————————————————————————————————————— fin

#———————————————————————————————————————— "missing" page is missing
#
# I believe that this is already taken care of with the last try/except
#
# if missing_page in request_path:
#   response = HttpResponse(missing_msg)
#   response.status_code = 404
#   return response
#
#———————————————————————————————————————— fin
