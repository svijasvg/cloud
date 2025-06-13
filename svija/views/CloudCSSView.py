
#———————————————————————————————————————— CloudCSSView.py

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from svija.models import Settings

def CloudCSSView(request):
    settings = get_object_or_404(Settings,enabled=True)
    color_main = settings.color_main
    color_accent = settings.color_accent
    color_dark = settings.color_dark

    response = "--main:{}; --accent:{}; --dark:{};"

    response = response.format(color_main, color_accent, color_dark)

    response = ":root { " +response + " }"

    return HttpResponse(response, content_type='text/css; charset=utf8')

#———————————————————————————————————————— fin

