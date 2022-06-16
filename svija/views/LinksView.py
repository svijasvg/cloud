#———————————————————————————————————————— LinksView.py

# return HttpResponse("debugging message.")

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from os.path import exists
from svija.models import Settings

import os

sync_folder = os.path.abspath(os.path.dirname(__name__)) + '/sync/'

def LinksView(request, request_prefix, placed_file):

#   return HttpResponse("debugging message: "+request_prefix+':'+placed_file)
    not_found = False

    img_path = sync_folder + request_prefix + '/' + placed_file
    bits = placed_file.split('.')
    type = bits[-1].lower()
    if type != 'png' and type != 'gif':
        type = 'jpeg'

#———————————————————————————————————————— does file exist?

    if not exists(img_path):
      img_path = os.getcwd() + '/static/svija/images/ff0000.'+ type
      not_found = True

#———————————————————————————————————————— return file contents

    image_data = open(img_path, "rb").read()
    response = HttpResponse(image_data, content_type='image/' + type)
    if not_found:
      response.status_code = 404
    return response

#———————————————————————————————————————— fin

