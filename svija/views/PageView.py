#   return HttpResponse("debugging message.")
#———————————————————————————————————————— svija.views

import os, os.path, sys, pathlib, svija 

from django.core.cache import cache
from django.db.models import Q
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render

from svija.models import *

from modules.add_script import *
from modules.attribute_scripts import *
from modules.cache_per_user import *
from modules.generate_accessibility import *
from modules.generate_form_js import *
from modules.generate_system_js import *
from modules.get_fonts import *
from modules.meta_canonical import *
from modules.page_load_svgs import *
from modules.sort_modules import *

#———————————————————————————————————————— view definition

@cache_per_user(ttl=60*60*24, cache_post=False)
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
    head_js = head_css = snippet   = svg           = ''
    html    = form     = modules   = body_js       = ''

    core_content = {
        'css'     : '',
        'head_js' : '',
        'body_js' : '',
        'svgs'    : '',
        'html'    : '',
        'form'    : '',
        'modules' : '',
    }

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

    #———————————————————————————————————————— sitewide scripts

    c, h, b, m, f = attribute_scripts(core_content, 'sitewide', page.shared.sharedscripts_set.all())
    head_css += c
    head_js  += h
    body_js  += b
    html     += m
    form     += f

    #———————————————————————————————————————— accessibility

    accessible = generate_accessibility(settings.url, Page.objects.all(), page)

    #———————————————————————————————————————— optional scripts

    c, h, b, m, f = attribute_scripts(core_content, 'optional', page.library_script.all())
    head_css += c
    head_js  += h
    body_js  += b
    html     += m
    form     += f

    #———————————————————————————————————————— page scripts

    c, h, b, m, f = attribute_scripts(core_content, 'page', page.pagescripts_set.all())

    head_css += c
    head_js  += h
    body_js  += b
    html     += m
    form     += f

    #———————————————————————————————————————— load all page svgs

    source_dir = 'sync/' + responsive.source_dir

    if page.override_dims:
        specified_width = page.width
    else:
        specified_width = responsive.width

    svg = ''
    all_svgs  = page.svg_set.all()

    res = page_load_svgs(all_svgs, source_dir, specified_width, use_p3)
    svg += res['svg']
    head_css += res['head_css']

    #———————————————————————————————————————— modules

    if page.suppress_modules == False:
    
        head_js += '\n\n//———————————————————————————————————————— prefix module scripts\n\n'
        body_js += '\n\n//———————————————————————————————————————— prefix module scripts\n\n'

        c, h, b, s, m, f = sort_modules(core_content, prefix.prefixmodules_set.all(), source_dir, specified_width, use_p3)
        head_css += c
        head_js  += h
        body_js  += b
        modules  += s
        html     += m
        form     += f

    head_js += '\n\n//———————————————————————————————————————— page module scripts\n\n'
    body_js += '\n\n//———————————————————————————————————————— page module scripts\n\n'

    all_modules = page.pagemodules_set.all()
    c, h, b, s, m, f = sort_modules(core_content, page.pagemodules_set.all(), source_dir, specified_width, use_p3)

    head_css += c
    head_js  += h
    body_js  += b
    modules  += s
    html     += m
    form     += f

    #———————————————————————————————————————— if there's a form, get form js
    # default string localization

    if form != '':
        head_js += generate_form_js(language)

    #———————————————————————————————————————— petit rappel

#   core_content = {
#       'css'     : '',
#       'head_js' : '',
#       'body_js' : '',
#       'svgs'    : '',
#       'html'    : '',
#       'form'    : '',
#       'modules' : '',
#   }

    #———————————————————————————————————————— page settings

    template = 'svija/' + page.template.filename
    if form != '': template = template.replace('.html', '_token.html')

    # set it up
    context = {
        'comments'      : comments,
        'title'         : title,
        'meta'          : meta,
        'fonts'         : font_link,
        'touch'         : touch,
        'system_js'     : system_js,
        'head_js'       : head_js,
        'css'           : head_css,
        'accessible'    : accessible,
        'svg'           : svg,
        'html'          : html,
        'form'          : form,
        'modules'       : modules,
        'analytics_id'  : analytics_id,
        'body_js'       : body_js
    }

    return render(request, template, context)

#———————————————————————————————————————— fin
