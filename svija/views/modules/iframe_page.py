
#:::::::::::::::::::::::::::::::::::::::: iframe_page.py

from django.http import HttpResponse
from django.core.cache import cache
from modules.cache_per_user import *
from django.shortcuts import get_object_or_404, render

@cache_per_user(60*60*24, False)
def iframe_page(request, section_code, request_slug):

  all_screens = "var all_screens = {0:'computer', 400:'mobile'}"
  current_path = "/"
  page_title = "This is the page title"

  context = {
    'all_screens'  : all_screens,
    'current_path' : current_path,
    'page_title'   : page_title,
  }

  template = 'svija/iframe.html'
  return render(request, template, context)

