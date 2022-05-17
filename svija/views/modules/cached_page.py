#———————————————————————————————————————— cached_page.py

#———————————————————————————————————————— notes
#
# from django.http import HttpResponse
# return HttpResponse("debugging message.")
#
#———————————————————————————————————————— import

import os, os.path, sys, pathlib, svija 

from django.core.cache import cache
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_protect

from svija.models import *
from PageObject import *

from modules.cache_per_user import *
from modules.combine_content import *
from modules.contains_form import *
from modules.default_screen_code import *
from modules.generate_accessibility import *
from modules.generate_form_js import *
from modules.generate_system_js import *
from modules.get_fonts import *
from modules.get_modules import *
from modules.get_page_modules import *
from modules.get_page_scripts import *
from modules.get_page_svgs import *
from modules.get_script import *
from modules.get_scripts import *
from modules.redirect_if_possible import *
from modules.scripts_to_page_obj import *

#———————————————————————————————————————— ▼ cached_page(request, language_code, request_slug, screen_code):
#
#   different according to screen code because screen code
#   has been appended to path

@cache_per_user(60*60*24, False)
@csrf_protect
def cached_page(request, language_code, request_slug, screen_code):

  page = Page.objects.filter(Q(language__code=language_code) & Q(screen__code=screen_code) & Q(url=request_slug) & Q(published=True)).first()
  if not page: raise Http404 # passed to file Error404.py

  #———————————————————————————————————————— main settings
  # https://stackoverflow.com/questions/5123839/fastest-way-to-get-the-first-object-from-a-queryset-in-django

  settings    = Settings.objects.filter(active=True).first()
  language    = Language.objects.filter(code=language_code).first()

  # now called screen
  responsive    = Screen.objects.filter(code=screen_code).first()

  use_p3      = settings.p3_color

  template    = 'svija/svija.html'
  accessible    = generate_accessibility(settings.url, Page.objects.all(), page)
  content_blocks  = []

  if page.override: page_width = page.width
  else:          page_width = responsive.width

  #———————————————————————————————————————— redirect if /en/home or /home

  redirect = redirect_if_possible(request, settings.language.code, language.default_page)

  if redirect: return HttpResponsePermanentRedirect(redirect)

  #———————————————————————————————————————— metatags, system js & fonts

  meta_fonts, font_css = get_fonts()

  screens = Screen.objects.order_by('pixels')

  system_js = generate_system_js(request.user, svija.views.version, settings, page, language_code, request_slug, responsive, screens)

  #———————————————————————————————————————— page SVG's and scripts

#   return HttpResponse("debugging message: "+str(page_width)) # 1200
  svgs, css_dimensions = get_page_svgs(screen_code, page, page_width, use_p3)

  content_blocks.append( scripts_to_page_obj('page', page.additionalscript_set.all(), svgs, css_dimensions))

  page_scripts_raw = page.pagescript_set.filter(active=True).order_by('order')
  page_scripts = get_page_scripts('page-specified scripts', page_scripts_raw)
  content_blocks.extend(page_scripts)

  #———————————————————————————————————————— page modules

  # pagemodule CONTAIN modules, but are not modules
  # can't use get_modules to get them because the modules are INSIDE pagemodule


  page_modules_raw = page.pagemodule_set.filter(active=True).order_by('zindex')
  page_modules = get_page_modules('page modules', page_modules_raw, language_code, screen_code, page, page_width, use_p3)

  content_blocks.extend(page_modules)

  #———————————————————————————————————————— "always include" modules

  if not page.suppress_modules:
    screen_modules = Module.objects.filter(Q(language__code=language_code) & Q(screen__code=screen_code) & Q(active=True) & Q(always=True)).order_by('order')
    module_content = get_modules('always-include modules', screen_modules, screen_code, page, page_width, use_p3)
    content_blocks.extend(module_content)

   #———————————————————————————————————————— "always include" scripts

  if not page.suppress_scripts:
    screen_scripts = Script.objects.filter(Q(active=True) & Q(always=True))
    script_content = get_scripts('always-include scripts', screen_scripts)
    content_blocks.extend(script_content)

  #———————————————————————————————————————— combine content blocks

  content_types = combine_content(content_blocks)

  #———————————————————————————————————————— if form, add CSRF token

  if contains_form(content_blocks):
    form_js = generate_form_js(language)
    template = template.replace('.html', '_token.html')
    content_types['js'] += "\n" + form_js

  #———————————————————————————————————————— template context

  context = {
    'comments'    : language.comment,
    'title'     : page.title + ' ' + language.title,
    'meta_fonts'  : meta_fonts,
    'touch'     : language.touch,
    'system_js'   : system_js,
    'font_css'    : font_css,
    'accessible'  : accessible,
    'analytics_id'  : settings.analytics_id,
  }

  context.update(content_types)

  #———————————————————————————————————————— ▲ return render

  return render(request, template, context)


#———————————————————————————————————————— fin
