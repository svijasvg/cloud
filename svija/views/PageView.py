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
from modules.redirect_if_home import *
from modules.get_modules import *

#———————————————————————————————————————— class definition

class page_obj():
    def __init__(self, meta_fonts, head_js, css, body_js, svgs, html, form):
        self.meta_fonts = meta_fonts
        self.head_js    = head_js
        self.css        = css
        self.body_js    = body_js
        self.svgs       = svgs
        self.html       = html
        self.form       = form

#———————————————————————————————————————— view definition

@cache_per_user(ttl=60*60*24, cache_post=False)
def PageView(request, request_prefix, request_slug):

    #———————————————————————————————————————— load objects

    prefix     = get_object_or_404(Prefix, path=request_prefix)
    page       = get_object_or_404(Page, Q(prefix__path=request_prefix) & Q(url=request_slug) & Q(visitable=True))
    responsive = get_object_or_404(Responsive, name=prefix.responsive.name)
    settings   = get_object_or_404(Settings, active=True)

    language   = prefix.language
    use_p3     = settings.p3_color
    source_dir = 'sync/' + responsive.source_dir

    if page.override_dims: page_width = page.width
    else:                  page_width = responsive.width
    
    #————————————————————————————————————————  redirect if it's a default page (path not shown)

    redirect = redirect_if_home(request_prefix, request.path, settings, prefix.default)
    if redirect: return HttpResponsePermanentRedirect(redirect)
    
    #———————————————————————————————————————— context for template

    meta_canon = system_js = accessible = ''

    core_content = {
        'meta_fonts':'', 'head_js':'', 'css':'', 'body_js':'', 'svgs':'', 'html':'', 'form':'', 'modules':'', }

    #———————————————————————————————————————— main content building

    # <meta rel="alternate" media="only screen and (max-width: 640px)" href="http://ozake.com/em/works" >
    meta_canon = meta_canonical(
        prefix,       responsive,     language,
        settings.url, request_prefix, request_slug, )

    # views.py generated JS
    system_js = generate_system_js(svija.views.version, language, settings, page, request_prefix, request_slug, responsive)

    # accessibility
    accessible = generate_accessibility(settings.url, Page.objects.all(), page)

    # fonts
    core_content = get_fonts(core_content)

    # load scripts
    core_content = attribute_scripts(core_content, 'sitewide', page.shared.sharedscripts_set.all())
    core_content = attribute_scripts(core_content, 'optional', page.library_script.all())
    core_content = attribute_scripts(core_content, 'page',     page.pagescripts_set.all())

#       self.meta_fonts = meta_fonts
#       self.head_js    = head_js
#       self.css        = css
#       self.body_js    = body_js
#       self.svgs       = svgs
#       self.html       = html
#       self.form       = form

    page_stuff, core_content = page_load_svgs(core_content,page, source_dir, page_width, use_p3)

    # modules

    if not page.suppress_modules:
        core_content = get_modules(core_content, 'prefix module scripts', prefix.prefixmodules_set.all(), source_dir, page_width, use_p3)

    core_content = get_modules(core_content, 'page module scripts', page.pagemodules_set.all(), source_dir, page_width, use_p3)

    # if there's a form, get form js
    core_content = generate_form_js(core_content, language)

    # get template (live, debug, or form with CSRF token)
    template = 'svija/' + page.template.filename
    if core_content['form'] != '': template = template.replace('.html', '_token.html')

    #———————————————————————————————————————— render it all

    context = {
        'comments'      : language.comment,
        'title'         : page.title + ' ' + language.title,
        'meta_canon'    : meta_canon,
        'touch'         : language.touch,
        'system_js'     : system_js,
        'accessible'    : accessible,
        'analytics_id'  : settings.analytics_id,
    }

    context.update(core_content)

    return render(request, template, context)

#———————————————————————————————————————— fin
