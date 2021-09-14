#———————————————————————————————————————— svija.views

# from django.http import HttpResponse
# return HttpResponse("debugging message.")

#———————————————————————————————————————— import

import os, os.path, sys, pathlib, svija 

from django.core.cache import cache
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render

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
#            'meta_canonical',     'redirect_if_home',         'scripts_to_page_obj', ]

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
from modules.get_modules import *
from modules.get_page_svgs import *
from modules.meta_canonical import *
from modules.redirect_if_home import *
from modules.scripts_to_page_obj import *
#rom modules.page_version import *
from django.http import Http404


#  ▼  ▲

#———————————————————————————————————————— main view definition

def PageView(request, request_prefix, request_slug):

  screen = request.COOKIES.get('screen')
  if (screen == None): 
    # calculate minimum screen
    screen = 'cp'
  return SubPageView(request, request_prefix, request_slug, screen)


#———————————————————————————————————————— ▼ cached view definition

@cache_per_user(60*60*24, False)
def SubPageView(request, request_prefix, request_slug, screen):

    #———————————————————————————————————————— main settings
    # https://stackoverflow.com/questions/5123839/fastest-way-to-get-the-first-object-from-a-queryset-in-django

    settings        = Settings.objects.filter(active=True).first()
    language        = Language.objects.filter(code=request_prefix).first()
    responsive      = Responsive.objects.filter(code=screen).first()

    #############################################################

    page            = Page.objects.filter(Q(language__code=request_prefix) & Q(screen__code=screen) & Q(url=request_slug) & Q(visitable=True)).first()
    if not page: raise Http404

        #eturn HttpResponse("page not found: " + request_prefix + ':' + screen + ':' + request_slug)

    # SHOULDN'T BE FIRST BECAUSE THAT ONLY GETS ONE SCRIPT WHEN THERE COULD BE SEVERA
    defaultscripts  = DefaultScripts.objects.filter(Q(responsive__code=screen) & Q(active=True)).first()

    use_p3          = settings.p3_color
    template        = 'svija/' + page.template.filename
    accessible      = generate_accessibility(settings.url, Page.objects.all(), page)
    content_blocks = []

    if page.override_dims: page_width = page.width
    else:                  page_width = responsive.width

    #———————————————————————————————————————— redirect if / or /en

    ################### LANGUAGE NEEDS A DEFAULT PAGE
    redirect = redirect_if_home(request_prefix, request.path, settings, language.default)
    if redirect: return HttpResponsePermanentRedirect(redirect)
    
    #———————————————————————————————————————— metatags, system js & fonts

    # <meta rel="alternate" media="only screen and (max-width: 640px)" href="http://ozake.com/em/works" >
    meta_canon = meta_canonical(
                      responsive,     language, settings.secure,
        settings.url, request_prefix, request_slug, )

    meta_fonts, font_css = get_fonts()

    screens = Responsive.objects.all()

    system_js = generate_system_js(svija.views.version, language, settings, page, request_prefix, request_slug, responsive, screens)
    system_js = '\n// screen=' + screen + '\n\n' + system_js

    #———————————————————————————————————————— default & optional scripts

    content_blocks.append( scripts_to_page_obj( 'default' , defaultscripts.defaultscripttypes_set.all(),'', '', ) )
    content_blocks.append( scripts_to_page_obj( 'optional', page.optional_script.all(), '', '', ) )

    #———————————————————————————————————————— page content

#   return HttpResponse("debugging message: "+str(page_width)) # 1200
    svgs, css_dimensions = get_page_svgs(page, page_width, use_p3)

    #———————————————————————————————————————— page scripts & modules

    content_blocks.append( scripts_to_page_obj('page', page.pagescripts_set.all(), svgs, css_dimensions))

    page_modules = get_modules('page modules', page.pagemodules_set.all(), page_width, use_p3)
    content_blocks.extend(page_modules)

    #———————————————————————————————————————— module content

#   if not page.suppress_modules:
#       all_modules = Module.objects.filter(Q(screen__code=screen) & Q(active=True) & Q(optional=False))
#       screen_modules  = get_modules('screen modules', all_modules, page_width, use_p3)
#       content_blocks.extend(screen_modules)

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
        'meta_canon'    : meta_canon,
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
