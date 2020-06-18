#———————————————————————————————————————— LinksView.py
# "links/accueil-bg-15097511.jpg"

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from svija.models import Prefix, PrefixModules, Settings

import os
SITE_ROOT = os.path.realpath(os.path.dirname(__file__)+'/../')

def LinksView(request, path1, placed_file):

    try:
        prefix = Prefix.objects.get(path=path1)
    except ObjectDoesNotExist:
        settings = get_object_or_404(Settings,active=True)
        prefix = settings.prefix

    responsive = prefix.responsive
    source_dir = 'sync/' + responsive.source_dir
    response = SITE_ROOT + source_dir +'/links/'+ placed_file

    source_dir = os.path.abspath(os.path.dirname(__name__)) + '/' + source_dir
    source_dir += '/links/' + placed_file
    bits = placed_file.split('.')
    type = bits[-1].lower()
    if type != 'png' and type != 'gif':
        type = 'jpg'
    image_data = open(source_dir, "rb").read()
    return HttpResponse(image_data, content_type='image/' + type)

def LinksViewHome(request, placed_file):
    settings = get_object_or_404(Settings,active=True)
    path1 = settings.prefix.path
    response = LinksView(request, path1, placed_file)
    return response

#———————————————————————————————————————— fin
