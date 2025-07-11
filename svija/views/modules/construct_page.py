
#:::::::::::::::::::::::::::::::::::::::: construct_page.py

#———————————————————————————————————————— notes
#
#   from django.http import HttpResponse
#   return HttpResponse("debugging message.")
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
from modules.create_other_screens import *
from modules.generate_links import *
from modules.generate_form_js import *
from modules.generate_system_js import *
from modules.get_accessible import *
from modules.integrate_fonts import *
from modules.font_css import *
from modules.get_modules import *
from modules.get_script_sets import *
from modules.get_page_svgs import *
from modules.get_script import *
from modules.redirect_if_possible import *
from modules.screen_redirect_js import *
from modules.scripts_to_page_obj import *
from modules.convert_modules import *
from modules.convert_script_sets import *
from modules.modules_dedupe import *
from modules.script_sets_dedupe import *
from modules.update_db import *

#   different according to screen code because screen code
#   has been appended to path

@cache_per_user(60*60*24, False)
@csrf_protect
def construct_page(request, section_url, page_url, screen_code, status_code):
# return HttpResponse(section_url +' : '+ page_url +' : '+ screen_code)

  #———————————————————————————————————————— do updates

  vb = update_db()
  if vb != False:
    return HttpResponse('<pre>' + vb + '<pre>')

# if update_db():
#   return HttpResponse("<pre>DATABASE UPDATED")

  #———————————————————————————————————————— get page

  page = Page.objects.filter(Q(section__code=section_url) & Q(screen__code=screen_code) & Q(url=page_url) & Q(published=True)).first()

  if not page:
    page = Page.objects.filter(Q(section__code='*') & Q(screen__code=screen_code) & Q(url=page_url) & Q(published=True)).first()

  if not page:
    page = Page.objects.filter(Q(section__code=section_url) & Q(screen__code='*') & Q(url=page_url) & Q(published=True)).first()

  if not page:
    page = Page.objects.filter(Q(section__code='*') & Q(screen__code='*') & Q(url=page_url) & Q(published=True)).first()

  if not page: raise Http404 # passed to file Error404.py

  #———————————————————————————————————————— main settings
  # https://stackoverflow.com/questions/5123839/fastest-way-to-get-the-first-object-from-a-queryset-in-django

  settings         = Settings.objects.filter(enabled=True).first()
  section          = Section.objects.filter(Q(code=section_url) & Q(enabled=True)).first()

  # now called screen
  responsive       = Screen.objects.filter(code=screen_code).first()

  use_p3           = settings.p3_color

  template         = 'svija/svija.html'
  accessible       = get_accessibility(page.accessibility_text)
  links, capture   = generate_links(settings.url, Page.objects.all(), page)
  page_blocks      = []
  module_blocks    = []

  if not page.default_dims: page_width = page.width
  else:          page_width = responsive.width

  #———————————————————————————————————————— redirect if /en/home or /home

  if page.url != 'missing':
    redirect = redirect_if_possible(request, settings.section.code, section.default_page)
    if redirect: return HttpResponsePermanentRedirect(redirect)

  #———————————————————————————————————————— metatags, system js & fonts

  language_code = ''

  if section.language:
    language_code = ' lang="'+ str(section.code) + '"'

# return HttpResponse("<pre>&lt;html" + language_code+"&gt;")

  integrate_fonts()
  google_font_meta, font_cssx = font_css()

  screens = Screen.objects.order_by('pixels')

  system_js = generate_system_js(request.user, svija.views.version, settings, page, section_url, page_url, responsive, screens)


  #———————————————————————————————————————— page SVG's and scripts

  # once something is appended to page_blocks, the order is set
  # so it has to be appended in the correct order

  # return HttpResponse("debugging message: "+str(page_width)) # 1200
  svgs, css_dimensions = get_page_svgs(screen_code, page, page_width, use_p3)

  # page SVG's
  page_blocks.append( scripts_to_page_obj('page', [], svgs, css_dimensions)) # append svg's w/dimensions

  # page additional scripts
  page_blocks.append( scripts_to_page_obj('page additional scripts', page.additionalscript_set.all(),'' , ''))

  #———————————————————————————————————————— script sets

  #eturn HttpResponse("debugging message: "+str)
  page_script_sets = list(page.pagescript_set.filter(enabled=True))
  all_script_sets = convert_script_sets(page_script_sets) # list of "Script" objects

  # Script Set "always include"
  if page.incl_scripts:
    default_scripts = Script.objects.filter(Q(enabled=True) & Q(always=True)).order_by('name')
    script_content = list(default_scripts)
    all_script_sets.extend(script_content)
    all_script_sets = script_sets_dedupe(all_script_sets)

  script_sets = get_script_sets('script sets', all_script_sets)

  #———————————————————————————————————————— set aside body js so Vibe executes last MOVE AFTER COMPONENTS	***********************

  script_sets_body_js = []
  for set in script_sets:
    new_set = page_obj('', '', set.body_js, '', '', '')
    script_sets_body_js.append(new_set)
    set.body_js = ''

  page_blocks.extend(script_sets)

  #———————————————————————————————————————— page modules

  # pagemodule CONTAIN modules, but are not modules
  # can't use get_modules to get them because the modules are INSIDE pagemodule

  # list of page modules, a different object than a simple module
  # connected by foreign keys
  page_modules = list(page.pagemodule_set.filter(enabled=True))

  # filters out incompatible modules & extracts module objects from page_module objects
  all_modules = convert_modules(page_modules, section_url, screen_code) # list of "Module" objects

  # always-include modules
  if page.incl_modules:
    default_modules = Module.objects.filter((Q(section__code=section_url)|Q(section__code='*'))  &  (Q(screen__code=screen_code)|Q(screen__code='*'))  &  Q(enabled=True)  &  Q(always=True))

    module_content = list(default_modules)
    all_modules.extend(module_content)
    all_modules = modules_dedupe(all_modules) 

  # added after default modules so they can display on top
  page_modules = get_modules('page modules', all_modules, section_url, screen_code, page, page_width, use_p3)

  module_blocks.extend(page_modules)

  #———————————————————————————————————————— script set body JS
  # at end of everything, so Vibed will execute last

  module_blocks.extend(script_sets_body_js)

  #———————————————————————————————————————— combine content blocks

  # both contain head_js, css, body

  page_content      = combine_content(page_blocks,      'page')
  module_content = combine_content(module_blocks, 'comp')

  #———————————————————————————————————————— if form, add CSRF token

  if contains_form(page_blocks):
    form_js = generate_form_js(section)
    template = template.replace('.html', '_token.html')
    page_content['page_head_js'] += "\n" + form_js

  #———————————————————————————————————————— template context

  ua = request.headers["User-Agent"]

  context = {
    'comments'         : section.comment,
    'language_code'    : language_code,
    'title'            : page.title + ' ' + section.title,
    'google_font_meta' : google_font_meta,
    'touch'            : section.touch,
    'system_js'        : system_js,
    'redirect_js'      : screen_redirect_js(ua),
    'font_css'         : font_cssx,
    'accessible'       : accessible,
    'links'            : links,
    'capture'          : capture,
    'analytics_id'     : settings.analytics_id,
  }

#   https://docs.djangoproject.com/en/5.1/ref/templates/api/
#
#   Context.update(other_dict)
#   In addition to push() and pop(), the Context object also defines an update() method.
#   This works like push() but takes a dictionary as an argument and
#   pushes that dictionary onto the stack instead of an empty one.

  context.update(page_content)
  context.update(module_content)


  return render(request, template, context, status=status_code)

#:::::::::::::::::::::::::::::::::::::::: fin

