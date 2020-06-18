#———————————————————————————————————————— RobotsView.py

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from svija.models import Settings

def RobotsView(request):
    settings = get_object_or_404(Settings,active=True)
    response = settings.robots.contents
    return HttpResponse(response, content_type='text/plain; charset=utf8')

#———————————————————————————————————————— fin
