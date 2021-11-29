#———————————————————————————————————————— PageView.py

#———————————————————————————————————————— debugging

# from django.http import HttpResponse
# return HttpResponse("debugging message.")

#———————————————————————————————————————— import

import os, os.path, sys, pathlib, svija 

from django.core.cache import cache
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_protect

from svija.models import *

#———————————————————————————————————————— class page_obj():

class page_obj():
    def __init__(self, head_js, css, body_js, svgs, html, form):
        self.head_js    = head_js
        self.css        = css
        self.body_js    = body_js
        self.svgs       = svgs
        self.html       = html
        self.form       = form
    def __getitem__(cls, x):
        return getattr(cls, x)

#———————————————————————————————————————— import

#mport importlib

# get list of modules from dir, not typing, prefix all with pageview_
#unctions = ['get_script',         'cache_per_user',           'combine_content',
#            'contains_form',      'generate_accessibility',   'generate_form_js',
#            'generate_system_js', 'get_fonts', 'get_modules', 'get_page_svgs',
#            'redirect_if_home',         'scripts_to_page_obj', ]

#or function in functions:
#   x = importlib.import_module('.'+function , 'modules')
#   getattr(x, function)


from modules.get_script import *
from modules.cache_per_user import *
from modules.combine_content import *
from modules.contains_form import *
from modules.generate_accessibility import *
from modules.generate_form_js import *
from modules.generate_system_js import *
from modules.get_fonts import *
from modules.get_page_modules import *
from modules.get_modules import *
from modules.get_page_svgs import *
from modules.get_screen_code import *
from modules.redirect_if_home import *
from modules.scripts_to_page_obj import *
#rom modules.page_version import *
from django.http import Http404

#———————————————————————————————————————— ▼ PageView(request, language_code, request_slug):
#
#   this method adds a screen code (/mb, /cp) to the request path
#   then calls the real pageview function, which is cached

# @never_cache
def PageView(request, language_code, request_slug):

  screen_code = get_screen_code(request)
  request.path += '/' + screen_code
  return SubPageView(request, language_code, request_slug, screen_code)

#———————————————————————————————————————— ▼ SubPageView(request, language_code, request_slug, screen_code):
#
#   different according to screen code because screen code
#   has been appended to path

@cache_per_user(60*60*24, False)
@csrf_protect
def SubPageView(request, language_code, request_slug, screen_code):

    #eturn HttpResponse("debugging message." + request.path)

    page = Page.objects.filter(Q(language__code=language_code) & Q(screen__code=screen_code) & Q(url=request_slug) & Q(visitable=True)).first()
    if not page: raise Http404 # passed to file Error404.py

    #———————————————————————————————————————— main settings
    # https://stackoverflow.com/questions/5123839/fastest-way-to-get-the-first-object-from-a-queryset-in-django

    settings        = Settings.objects.filter(active=True).first()
    language        = Language.objects.filter(code=language_code).first()

    # now called screen
    responsive      = Responsive.objects.filter(code=screen_code).first()

    use_p3          = settings.p3_color

    # deprecated
    #emplate        = 'svija/' + page.template.filename

    template        = 'svija/svija.html'
    accessible      = generate_accessibility(settings.url, Page.objects.all(), page)
    content_blocks  = []

    if page.override_dims: page_width = page.width
    else:                  page_width = responsive.width

    #———————————————————————————————————————— redirect if /en/home or /en or /fr/accueil

    redirect = redirect_if_home(request.path, settings.language.code, language.default)
    if redirect: return HttpResponsePermanentRedirect(redirect)

    #———————————————————————————————————————— metatags, system js & fonts

    meta_fonts, font_css = get_fonts()

    screens = Responsive.objects.order_by('limit')

    system_js = generate_system_js(svija.views.version, settings, page, language_code, request_slug, responsive, screens)
    system_js = '// '+request.path + '\n// '+request_slug + '\n//' + screen_code + system_js

    #———————————————————————————————————————— page SVG's & scripts

#   return HttpResponse("debugging message: "+str(page_width)) # 1200
    svgs, css_dimensions = get_page_svgs(screen_code, page, page_width, use_p3)

    content_blocks.append( scripts_to_page_obj('page', page.pagescripts_set.all(), svgs, css_dimensions))

    #———————————————————————————————————————— scripts

    page_scripts_raw = page.default_scripts.all().filter(active=True)
    for this_set in page_scripts_raw:
      content_blocks.append( scripts_to_page_obj( 'scripts' , this_set.defaultscripttypes_set.all(),'', '', ) )

#   deprecated
#   content_blocks.append( scripts_to_page_obj( 'default' , defaultscripts.defaultscripttypes_set.all(),'', '', ) )
#   content_blocks.append( scripts_to_page_obj( 'optional', page.optional_script.all(), '', '', ) )

    #———————————————————————————————————————— page modules

    # pagemodules CONTAIN modules, but are not modules
    # can't use get_modules to get them because the modules are INSIDE pagemodules

    page_modules_raw = page.pagemodules_set.filter(active=True).order_by('zindex')
    page_modules = get_page_modules('page modules', page_modules_raw, language_code, screen_code, page, page_width, use_p3)
    content_blocks.extend(page_modules)

    #———————————————————————————————————————— modules

    if not page.suppress_modules:
        screen_modules = Module.objects.filter(Q(language__code=language_code) & Q(screen__code=screen_code) & Q(published=True) & Q(optional=True)).order_by('display_order')
        module_content = get_modules('screen modules', screen_modules, screen_code, page, page_width, use_p3)
        content_blocks.extend(module_content)

    #———————————————————————————————————————— combine content blocks

    content_types = combine_content(content_blocks)

    #———————————————————————————————————————— if form, add CSRF token

    if contains_form(content_blocks):
        form_js = generate_form_js(language)
        template = template.replace('.html', '_token.html')
        content_types['js'] += "\n" + form_js

    #———————————————————————————————————————— template context

    context = {
        'comments'      : language.comment,
        'title'         : page.title + ' ' + language.title,
        'meta_fonts'    : meta_fonts,
        'touch'         : language.touch,
        'system_js'     : system_js,
        'font_css'      : font_css,
        'accessible'    : accessible,
        'analytics_id'  : settings.analytics_id,
    }

    context.update(content_types)

    #———————————————————————————————————————— ▲ return render

    return render(request, template, context)


#———————————————————————————————————————— fin
