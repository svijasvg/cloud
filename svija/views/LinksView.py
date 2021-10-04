#———————————————————————————————————————— LinksView.py

# return HttpResponse("debugging message.")

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from svija.models import Prefix, PrefixModules, Settings

import os

sync_folder = os.path.abspath(os.path.dirname(__name__)) + '/sync/'

def LinksView(request, request_prefix, placed_file):

    # full path is in request.path for free

    # home page image path ../../links/demo-only-big-29258056.jpg

#   return HttpResponse("⚠️ " + sync_folder + request_prefix + '/' + placed_file)

#   try:
#       prefix = Prefix.objects.get(path=request_prefix)
#   except ObjectDoesNotExist:
#       settings = get_object_or_404(Settings,active=True)
#       prefix = settings.prefix

#   source_dir = os.path.abspath(os.path.dirname(__name__)) + '/sync'
#   source_dir += '/Links/' + placed_file

    source_dir = sync_folder + request_prefix + '/' + placed_file
    bits = placed_file.split('.')
    type = bits[-1].lower()
    if type != 'png' and type != 'gif':
        type = 'jpeg'

#———————————————————————————————————————— return file contents

    image_data = open(source_dir, "rb").read()
    return HttpResponse(image_data, content_type='image/' + type)

#ef LinksViewHome(request, placed_file):
#   settings = get_object_or_404(Settings,active=True)
#   request_prefix = settings.prefix.path
#   response = LinksView(request, request_prefix, placed_file)
#   return response

#———————————————————————————————————————— fin
