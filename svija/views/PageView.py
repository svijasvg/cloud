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
    def __getitem__(cls, x):
        return getattr(cls, x)

from modules.get_modules import *
from modules.order_content import *

#———————————————————————————————————————— view definition

@cache_per_user(ttl=60*60*24, cache_post=False)
def PageView(request, request_prefix, request_slug):

    all_modules = []

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
    # meta_fonts & css
    #ore_content = get_fonts(core_content)
    meta_fonts, font_css = get_fonts()

    # load scripts
    #ore_content = attribute_scripts(core_content, 'sitewide', page.shared.sharedscripts_set.all())
    #ore_content = attribute_scripts(core_content, 'optional', page.library_script.all())
    #ore_content = attribute_scripts(core_content, 'page',     page.pagescripts_set.all())

    head_js, css, body_js, html, form = attribute_scripts('sitewide', page.shared.sharedscripts_set.all())
    head_js, css, body_js, html, form = attribute_scripts('optional', page.library_script.all())
    head_js, css, body_js, html, form = attribute_scripts('page',     page.pagescripts_set.all())

    # page content & modules

    page_stuff = page_load_svgs(page, source_dir, page_width, use_p3)
    all_modules.append(page_stuff)

    if not page.suppress_modules:
        prefix_modules  = get_modules('prefix module', prefix.prefixmodules_set.all(), source_dir, page_width, use_p3)
        all_modules.extend(prefix_modules)

    page_modules = get_modules('page module', page.pagemodules_set.all(), source_dir, page_width, use_p3)
    all_modules.extend(page_modules)


    # if there's a form, get form js
    #ore_content = generate_form_js(core_content, language)

    # get template (live, debug, or form with CSRF token)
    template = 'svija/' + page.template.filename
    if core_content['form'] != '':
        form_js = generate_form_js(language)
        template = template.replace('.html', '_token.html')

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

    page_blocks = order_content(all_modules)
    context.update(page_blocks)

    return render(request, template, context)

#———————————————————————————————————————— fin
