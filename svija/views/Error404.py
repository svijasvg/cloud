#———————————————————————————————————————— Error404.py

#———————————————————————————————————————— notes
#
#   the basic point is to see if:
#
#   1. is it an admin page? send to admin home
#   2. is it an image? return image error
#   3. is it a redirect? do that
#   4. can we determine the the section? use that
#   5. get default section
#
#   https://websiteadvantage.com.au/404-Error-Handler-Checker
#
#
#   /fr/accueilx/cp
#   /fr/accueilx
#   /fr
#   /accueilx
#   /Links/lmkjs
#   /images/lkjmlkj
#
#   if we split it by slash:
#   - the first part may be a section code
#
# from django.http import HttpResponse
# return HttpResponse("debugging message.")
#
#———————————————————————————————————————— imports

from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse, HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from modules.cached_page import *
from svija.models import Screen, Redirect, Section, Settings
import re
import os

#———————————————————————————————————————— Error404(request, *args, **kwargs):

#@never_cache # we'll see if this is a problem
def Error404(request, *args, **kwargs):

#———————————————————————————————————————— variables

  missing_image       = '<pre>\n\n   missing image'
  msg_broken          = '<pre>\n\n   Configuration Error\n\n   Please contact support@svija.com.'
  msg_missing         = '<pre>\n\n   Page Missing\n\n   To customize this message, add a page called "missing" to this section.'
  msg_missing        +=      '\n\n   There should be a "missing" page for each screen size.'

  missing_page_exists = False
  section_code        = ''

#———————————————————————————————————————— 1. is it an admin page?

  if request.path[0:6] == '/admin':
    return HttpResponsePermanentRedirect('/admin/svija/')

#———————————————————————————————————————— 2. is it an image?
# see also LinksView.py

  pf = '.+\.(jpeg|jpg|png|gif)$'
  img_file = request.path

  if re.search(pf, request.path):
    ext      = img_file.split('.')[-1].lower()
    img_path = os.getcwd() + '/static/svija/images/ff0000.'+ ext
    img      = open(img_path, 'rb')

    response = FileResponse(img)
    response.status_code = 404
    return response

#———————————————————————————————————————— 3. is it a redirect?

  try:
    redirect_obj = Redirect.objects.get(from_url=request.path, active=True)
    return HttpResponsePermanentRedirect(redirect_obj.to_url)
  except ObjectDoesNotExist: pass


#:::::::::::::::::::::::::::::::::::::::: it's definitely a missing page

#———————————————————————————————————————— 4. is there a valid section code?

  section_code = request.path[1:].split('/')[0]

  if section_code != '':
    try:
      section = Section.objects.get(code=section_code)
    except:
      section_code = ''

#———————————————————————————————————————— 5. get default if not

  if section_code == '':
    try:
      section_code = Settings.objects.get(active=True).section.code
    except:
      response             = HttpResponse(msg_broken)
      response.status_code = 404
      return response

#———————————————————————————————————————— 6. is there a valid screen code in a cookie?

  screen_code = request.COOKIES.get('screen_code')
  if screen_code == None: screen_code = ''
 
  if screen_code != '':
    try:
      screen = Screen.objects.get(code=screen_code)
    except:
      pass

#———————————————————————————————————————— 7. get default if not

  if screen_code == '':
    try:
      screen_code = Screen.objects.first().code
    except:
      response             = HttpResponse(msg_broken)
      response.status_code = 404
      return response

#———————————————————————————————————————— have valid screen & section; get "missing" page

  try:
    response = cached_page(request, section_code, 'missing', screen_code)
  except:
    response = HttpResponse(msg_missing)

  response.status_code = 404
  return response


#———————————————————————————————————————— fin
