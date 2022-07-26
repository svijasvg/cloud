#———————————————————————————————————————— LinksView.py
#
#   NOTE: missing images are 1x1 — barely visible in the browser
#
#   Links folder redirection breaks if the prefix does not exist
#   instead of defaulting to en, need to get site default section
#
# return HttpResponse("debugging message.")

from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
#rom modules.missing_image import *
from os.path import exists
from svija.models import Settings

import os

def LinksView(request, request_prefix, img_file):


#———————————————————————————————————————— path

  sync_folder = os.path.abspath(os.path.dirname(__name__)) + '/sync/'
  img_path    = sync_folder + request_prefix + '/' + img_file

#———————————————————————————————————————— does file exist?

  if not exists(img_path):
    ext      = img_file.split('.')[-1].lower()
    img_path = os.getcwd() + '/static/svija/images/ff0000.'+ ext
    img      = open(img_path, 'rb')

    response = FileResponse(img)
    response.status_code = 404
    return response

#———————————————————————————————————————— return file contents

  img = open(img_path, 'rb')
  response = FileResponse(img)
  return response


#———————————————————————————————————————— fin
