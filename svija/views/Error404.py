#   return HttpResponse("debugging message.")
#———————————————————————————————————————— 404 error
# https://websiteadvantage.com.au/404-Error-Handler-Checker

# Links folder redirection breaks if the prefix does not exist
# instead of defaulting to en, need to get site default language

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache

from svija.models import Forwards, Language, Settings
from svija.views import PageView

@never_cache
def Error404(request, *args, **kwargs):

  # remove leading slash
  requested = request.path[1:]
  missing_page = 'missing'

#———————————————————————————————————————— check for redirect

  # 3 cases:
  # external site, starts with http or https
  # internal address, with prefix like /fr/
  # internal address, with no prefix like /admin/svija/help/

  try:
    redirect_obj = Forwards.objects.get(from_url=requested, active=True)

    if redirect_obj.to_prefix[0:4] == 'http': # or https
      return HttpResponsePermanentRedirect(redirect_obj.to_prefix + '://' + redirect_obj.to_page)
    elif redirect_obj.to_prefix != '':
      return HttpResponsePermanentRedirect('/'+redirect_obj.to_prefix + '/' + redirect_obj.to_page)
    else:
      return HttpResponsePermanentRedirect('' + redirect_obj.to_page)

  except ObjectDoesNotExist: pass

#———————————————————————————————————————— if we're already on the "missing" page

  if missing_page in requested:
    response = HttpResponse('<pre>\n\n   Page Missing: ' + requested + '\n\n   To customize this message, add a page called "' + missing_page + '".')
    response.status_code = 404
    return response

#———————————————————————————————————————— get language if possible

  requested_code = 'none'

  if '/' in requested:
    requested_code = request.path.split('/')[1]
  
  try:
    lang = Language.objects.get(code=requested_code)
  except ObjectDoesNotExist:
    settings = get_object_or_404(Settings,active=True)
    lang = settings.language.code

#———————————————————————————————————————— get screen if possible

  # don't need screen code, handled by PageView

#———————————————————————————————————————— update the request.path to missing

  request.path = '/' + lang + '/' + missing_page

#———————————————————————————————————————— return correct missing page

  response = PageView(request, lang, missing_page,)
  response.status_code = 404

  return response

#———————————————————————————————————————— fin
