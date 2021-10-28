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

from svija.models import Forwards, Language, Settings
from svija.views import SubPageView

from modules.get_screen_code import *

#———————————————————————————————————————— Error404(request, *args, **kwargs):

#@never_cache # we'll see if this is a problem
def Error404(request, *args, **kwargs):

  request_path = request.path[1:-1] # remove leading slash

  missing_page = 'missing'
  missing_msg = '<pre>\n\n   Page Missing\n\n   To customize this message, add a page called "' + missing_page + '".'

#———————————————————————————————————————— check for redirect

  # 3 cases:

  # external site, starts with http or https
  # internal address, with prefix like /fr/
  # internal address, with no prefix like /admin/svija/help/

  # redirects will pass by HomeView.py first as a possible language code
  # that will add a trailing slash

  try:
    redirect_obj = Forwards.objects.get(from_url=request_path, active=True)
    return HttpResponsePermanentRedirect(redirect_obj.to_page)
  except ObjectDoesNotExist: pass

  try:
    redirect_obj = Forwards.objects.get(from_url='/'+request_path, active=True)
    return HttpResponsePermanentRedirect(redirect_obj.to_page)
  except ObjectDoesNotExist: pass

#———————————————————————————————————————— "missing" page is missing

  if missing_page in request_path:
    response = HttpResponse(missing_msg)
    response.status_code = 404
    return response

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

  screen_code = get_screen_code(request)

#———————————————————————————————————————— update the request.path to missing

  request.path = '/' + language_code + '/' + missing_page + '/' + screen_code

#———————————————————————————————————————— return correct missing page

  try:
    response = SubPageView(request, language_code, missing_page, screen_code)

  except:
    response = HttpResponse(missing_msg)
    #esponse = HttpResponse(request.path)

  response.status_code = 404
  return response


#———————————————————————————————————————— fin
