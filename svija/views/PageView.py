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

from modules import cache_functions, meta_canonical, make_snippet 
from modules.sort_modules import *
from modules.page_load_svgs import *
from modules.add_script import *

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

    comments      = ''
    title         = ''
    meta          = ''
    fonts         = ''
    touch         = ''
    view_js       = ''
    user_js       = ''
    head_css      = ''
    snippet       = ''
    svg           = ''
    html          = ''
    form          = ''
    module        = ''
    analytics_id  = ''
    body_js       = ''

    #———————————————————————————————————————— the easy ones

    comments     = language.comment
    title        = page.title + ' ' + language.title
    touch        = language.touch
    analytics_id = settings.analytics_id
    use_p3       = settings.p3_color

    #———————————————————————————————————————— meta tag

    # just send necessary parts, not whole objects
    # creates meta link to canonical page
    #  <meta rel="alternate" media="only screen and (max-width: 640px)" href="http://ozake.com/em/works" >

    meta  = meta_canonical.create_canonical(
        prefix,
        responsive,
        language,
        settings.url,
        request_prefix,
        request_slug,
    )

    #———————————————————————————————————————— fonts
    # should be first in CSS

    font_objs = Font.objects.all()
    css_str  = "@font-face {{ font-family:'{}'; src:{}'){}; }}"
    link_str = '\n  <link rel="stylesheet" href="{}" />'
    font_css = ''
    font_link = ''
    google_fonts = []

    for this_font in font_objs:
        if this_font.active:
            font_face = this_font.css
            font_src  = this_font.source

            if this_font.google:
                req = this_font.style.lower().replace(' ','')
                req = this_font.family.replace(' ','+') + ':' + req 
                google_fonts.append(req)

            elif font_src.find('woff2') > 0:
                font_format = " format('woff2')"
                font_src = "url('/fonts/" + font_src
                font_css  += '\n'+ css_str.format(font_face, font_src, font_format)

            elif font_src.find('woff') > 0:  
                font_format = " format('woff')"
                font_src = "url('/fonts/" + font_src
                font_css += '\n'+ css_str.format(font_face, font_src, font_format)

            elif font_src.find(',') > 0: # local fonts
                # src: local('Arial'), local('Arial MT'), local('Arial Regular'); }
                font_format = ''
                locals = font_src.replace(', ',',').split(',')
                font_src = "local('"+"'), local('".join(locals)
                font_css += '\n'+ css_str.format(font_face, font_src, font_format)

    head_css = font_css + head_css

    if len(google_fonts) > 0:
        link_str = '  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family={}">'
        font_link = link_str.format(('|').join(google_fonts))

    #———————————————————————————————————————— views.py generated JS

    # version information
    view_js += "var svija_version='2.1.5';\n"

    # language information
    cde = language.code
    view_js += 'var language_code = "' + cde +'";\n'
#   pfx = settings.prefix.path
#   view_js += 'var default_site_prefix = "' + pfx +'";\n'

    # accept cookies by default
    if settings.tracking_on:
        view_js += "var tracking_on = true;\n"
    else:
        view_js += "var tracking_on = false;\n"

    # page url
    if settings.secure:
        page_url = 'https://'
    else:
        page_url = 'http://'

    page_url += settings.url + '/' + request_prefix + '/' + request_slug
    view_js += "var page_url = '" + page_url + "';\n"

    # page dimension information
    dim_js = ''

    if page.override_dims:
        dim_js += '// overridden in page settings:\n'

        dim_js += 'var page_width = '     + str(page.width  ) + '; '
        dim_js += 'var visible_width = '  + str(page.visible) + '; \n'
        dim_js += 'var page_offsetx = '   + str(page.offsetx) + '; '
        dim_js += 'var page_offsety = '   + str(page.offsety) + '; \n'

    else:
        dim_js += 'var page_width = '     + str(responsive.width)   + '; '
        dim_js += 'var visible_width = '  + str(responsive.visible) + '; \n'
        dim_js += 'var page_offsetx = '   + str(responsive.offsetx) + '; '
        dim_js += 'var page_offsety = '   + str(responsive.offsety) + '; \n'

    view_js += dim_js

    #———————————————————————————————————————— form-oriented language variables

    # added down below if there is a form

    form_js = '\n//———————————————————————————————————————— mail form\n\n'

    form_js += 'var name_init = "'      + language.form_name       + '";\n'
    form_js += 'var address_init = "'   + language.form_email      + '";\n'
    form_js += 'var status_init = "'    + language.form_status     + '";\n'
    form_js += 'var send_init = "'      + language.form_send       + '";\n'
    form_js += 'var mess_sending = "'   + language.form_sending    + '";\n'
    form_js += 'var mess_received = "'  + language.form_rcvd       + '";\n'
    form_js += 'var alert_received = "' + language.form_alert_rcvd + '";\n'
    form_js += 'var alert_failed = "'   + language.form_alert_fail  + '";\n'

#var address_failed = 'cxoxnxtxaxcxtx@xoxzxaxkxex.xcxom';

#var alert_failed   = 'Your message could not be sent.\n\nPlease send it directly to '
#                   + address_failed.replace(/x/g,'');

    alert_char  = 'x' # should be calculated
    alert_email = alert_char.join(list(language.email))

    form_js += 'var alert_email  = "'   + alert_email + '";\n'
    form_js += 'var alert_char   = "'   + alert_char  + '";\n'
    form_js += '\n//———————————————————————————————————————— /mail form\n\n'

    #———————————————————————————————————————— shared scripts

    user_js += '\n//———————————————————————————————————————— shared scripts\n'
    body_js += '//———————————————————————————————————————— shared scripts'

    shared = page.shared.sharedscripts_set.all()  

    for this_script in shared:
        if this_script.type == 'CSS' and this_script.active == True:
            head_css += add_script('css', this_script.name, this_script.content)

        if this_script.type == 'head JS' and this_script.active == True:
            user_js += add_script('js', this_script.name, this_script.content)

        if this_script.type == 'body JS' and this_script.active == True:
            body_js += add_script('js', this_script.name, this_script.content)

    #———————————————————————————————————————— snippet

    text = page.snippet_text
    links = make_snippet.create(settings.url, Page.objects.all())
    capture = '/images/capture.jpg'

    tag = '{0}\n\n{1}<a href=http://{2}><img src={3}></a>'
    snippet = tag.format(text,links,settings.url,capture)

    #———————————————————————————————————————— library scripts

#   html     = ''
#   form     = ''
    user_js += '\n\n//———————————————————————————————————————— library scripts\n\n'
    body_js += '\n\n//———————————————————————————————————————— library scripts\n\n'

    all_scripts = page.library_script.all()

    for this_script in all_scripts:
        if this_script.type == 'head JS':
            user_js += add_script('js', this_script.name, this_script.content)

        if this_script.type == 'body JS':
            body_js += add_script('js', this_script.name, this_script.content)

        if this_script.type == 'CSS':
            head_css += add_script('css', this_script.name, this_script.content)

        if this_script.type == 'HTML':
            html += add_script('html', this_script.name, this_script.content)

        if this_script.type == 'form':
            form += add_script('html', this_script.name, this_script.content)

    #———————————————————————————————————————— page scripts

    html     = ''
    form     = ''
    user_js += '\n\n//———————————————————————————————————————— page scripts\n\n'
    body_js += '\n\n//———————————————————————————————————————— page scripts\n\n'

    all_scripts = page.pagescripts_set.all()

    for this_script in all_scripts:
        if this_script.type == 'head JS' and this_script.active == True:
            user_js += add_script('js', this_script.name, this_script.content)

        if this_script.type == 'body JS' and this_script.active == True:
            body_js += add_script('js', this_script.name, this_script.content)

        if this_script.type == 'CSS' and this_script.active == True:
            head_css += add_script('css', this_script.name, this_script.content)

        if this_script.type == 'HTML' and this_script.active == True:
            html += add_script('html', this_script.name, this_script.content)

        if this_script.type == 'form' and this_script.active == True:
            form += add_script('html', this_script.name, this_script.content)

    if form != '': user_js += form_js

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
        'view_js'       : view_js,
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
