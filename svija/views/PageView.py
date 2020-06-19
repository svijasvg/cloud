#   return HttpResponse("debugging message.")
#———————————————————————————————————————— svija.views

import os, os.path, sys, pathlib, svija 

from django.contrib.staticfiles.views import serve
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.views.decorators.cache import never_cache

from svija.models import Forwards, Font, Notes, Language, Responsive, Robots
from svija.models import Template, LibraryScript, Module, ModuleScripts
from svija.models import Shared, SharedScripts
from svija.models import Prefix, PrefixModules
from svija.models import Settings
from svija.models import Page, PageScripts, Svg, PageModules

from modules import cache_functions
from modules.meta_canonical import *
from modules.sort_modules import *
from modules.page_load_svgs import *
from modules.add_script import *
from modules.get_fonts import *
from modules.generate_system_js import *
from modules.generate_form_js import *
from modules.generate_sitewide_js import *
from modules.generate_accessibility import *
from modules.generate_optional_js import *
from modules.generate_page_js import *

from django.http import HttpResponsePermanentRedirect

#———————————————————————————————————————— view definition

@cache_functions.cache_per_user_function(ttl=60*60*24, cache_post=False)
def PageView(request, request_prefix, request_slug):

    #———————————————————————————————————————— load objects

    prefix     = get_object_or_404(Prefix, path=request_prefix)
    page       = get_object_or_404(Page, Q(prefix__path=request_prefix) & Q(url=request_slug) & Q(visitable=True))
    responsive = get_object_or_404(Responsive, name=prefix.responsive.name)
    settings   = get_object_or_404(Settings, active=True)
    language   = prefix.language

    #————————————————————————————————————————  redirect if it's a default page (path not shown)

    site_default_prefix = '/' + settings.prefix.path +'/'            # default prefix for site
    site_default_slug   = settings.prefix.default                    # default slug for prefix
    site_default_path   = site_default_prefix + site_default_slug    # default slug for prefix

    this_prefix         = '/' + request_prefix +'/'
    this_prefix_default    = this_prefix + prefix.default

    # if address corresponds to site default page
    if request.path == site_default_path or request.path == site_default_prefix:
        return HttpResponsePermanentRedirect('/')

    # if address corresponds to prefix default page
    if request.path == this_prefix_default:
        return HttpResponsePermanentRedirect(this_prefix)

    #———————————————————————————————————————— context for template

    comments     = language.comment
    title        = page.title + ' ' + language.title
    touch        = language.touch
    analytics_id = settings.analytics_id
    use_p3       = settings.p3_color

    #———————————————————————————————————————— more context for template

    meta    = fonts    = font_link = system_js     = ''
    user_js = head_css = snippet   = svg           = ''
    html    = form     = module    = body_js       = ''

    #———————————————————————————————————————— meta tag
    # meta link to canonical page
    #  <meta rel="alternate" media="only screen and (max-width: 640px)" href="http://ozake.com/em/works" >

    meta = meta_canonical(
        prefix,       responsive,     language,
        settings.url, request_prefix, request_slug, )

    #———————————————————————————————————————— fonts
    # should be first in CSS

    font_link, font_css = get_fonts()
    head_css = font_css + head_css

    #———————————————————————————————————————— views.py generated JS

    system_js = generate_system_js(svija.views.version, language, settings, page, request_prefix, request_slug, responsive)

    #———————————————————————————————————————— form-oriented language variables
    # added to user js only if there is a form

    form_js = generate_form_js(language)

    #———————————————————————————————————————— sitewide scripts

    c, h, b, m, f = generate_sitewide_js(page.shared.sharedscripts_set.all())
    head_css += c
    user_js  += h
    body_js  += b
#   html     += m
#   form     += f

    #———————————————————————————————————————— snippet

    snippet = generate_accessibility(settings.url, Page.objects.all(), page)

    #———————————————————————————————————————— optional scripts

    c, h, b, m, f = generate_optional_js(page.library_script.all())
    head_css += c
    user_js  += h
    body_js  += b
#   html     += m
#   form     += f

    #———————————————————————————————————————— page scripts

    c, h, b, m, f = generate_page_js(page.pagescripts_set.all())

    head_css += c
    user_js  += h
    body_js  += b
    html     += m
    form     += f

    #———————————————————————————————————————— load all svgs

    if form == '': form_js = ''
    user_js += form_js

    #———————————————————————————————————————— load all svgs

    source_dir = 'sync/' + responsive.source_dir

    if page.override_dims:
        specified_width = page.width
    else:
        specified_width = responsive.width

    svg = ''
    all_svgs  = page.svg_set.all()

    thisThing = page_load_svgs(all_svgs, source_dir, specified_width, use_p3)
    svg += thisThing['svg']
    head_css += thisThing['head_css']

    #———————————————————————————————————————— modules

    if page.suppress_modules == False:
    
        user_js += '\n\n//———————————————————————————————————————— prefix module scripts\n\n'
        body_js += '\n\n//———————————————————————————————————————— prefix module scripts\n\n'

        thisThing = sort_modules(prefix.prefixmodules_set.all(), source_dir, specified_width, use_p3)
        module += thisThing['svg']
        head_css += thisThing['head_css']
        user_js += thisThing['head_js']
        body_js += thisThing['body_js']
        html    += thisThing['html']
        form    += thisThing['form']

    user_js += '\n\n//———————————————————————————————————————— page module scripts\n\n'
    body_js += '\n\n//———————————————————————————————————————— page module scripts\n\n'

    all_modules = page.pagemodules_set.all()

    thisThing = sort_modules(page.pagemodules_set.all(), source_dir, specified_width, use_p3)
    module += thisThing['svg']
    head_css += thisThing['head_css']
    user_js += thisThing['head_js']
    body_js += thisThing['body_js']
    html    += thisThing['html']
    form    += thisThing['form']

    #———————————————————————————————————————— page settings

    template = 'svija/' + page.template.filename

    if form != '':
        template = template.replace('.html', '_token.html')

    # set it up
    context = {
        'comments'      : comments,
        'title'         : title,
        'meta'          : meta,
        'fonts'         : font_link,
        'touch'         : touch,
        'system_js'       : system_js,
        'user_js'       : user_js,
        'css'           : head_css,
        'snippet'       : snippet,
        'svg'           : svg,
        'html'          : html,
        'form'          : form,
        'module'        : module,
        'analytics_id'  : analytics_id,
        'body_js'       : body_js
    }

    return render(request, template, context)
#   return render(request, template, {'context':context})

#———————————————————————————————————————— fin
