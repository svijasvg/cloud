#   return HttpResponse("debugging message.")
#———————————————————————————————————————— svija.views

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.views.decorators.cache import never_cache
from django.core.exceptions import ObjectDoesNotExist

from .models import Language, Responsive, Robots, Template, Prefix, Settings
from .models import Shared, SharedScripts 
from .models import Menu, MenuScripts
from .models import Page, PageScripts, LibraryScript, Svg
from .models import Redirect

from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.core.files import File
from django.core.cache import cache
import os.path
import sys
import pathlib

#from django.views import static
import os
SITE_ROOT = os.path.realpath(os.path.dirname(__file__)+'/../')
from django.contrib.staticfiles.views import serve

#———————————————————————————————————————— page (with embedded svg)

path = os.path.abspath(os.path.join(os.path.dirname(__file__), './'))
#path = os.path.abspath(os.path.join(os.path.dirname(__file__), './modules'))
if not path in sys.path: sys.path.insert(1, path)

#add the path to the module to sys.path before the import statement which raises the exception within the offending pr
#add the path to the module to myproject.wsgi for applications using WSGI,
#import modules
import svija 
from django.db.models import Q

#———————————————————————————————————————— / was requested

from django.shortcuts import redirect
def HomePage(request, path1):

    if path1 == '':
        settings = get_object_or_404(Settings,active=True)
        path1 = settings.prefix.path

    prefix = get_object_or_404(Prefix, path=path1)
    path2 = prefix.default

    response = PageView(request, path1, path2,)
    return response

#———————————————————————————————————————— robots.txt

from .models import Robots

def RobotsView(request):
    settings = get_object_or_404(Settings,active=True)
    response = settings.robots.contents
    return HttpResponse(response, content_type='text/plain; charset=utf8')

#———————————————————————————————————————— sitemap.txt

from modules import sitemap

def SitemapView(request):
    settings = get_object_or_404(Settings,active=True)
    domain = settings.url
    response = sitemap.create(domain, Page.objects.all())
    return HttpResponse(response, content_type='text/plain; charset=utf8')

#———————————————————————————————————————— placed images
# "Links/accueil-bg-15097511.jpg"

def LinksView(request, path1, placed_file):

    try:
        prefix = Prefix.objects.get(path=path1)
    except ObjectDoesNotExist:
        settings = get_object_or_404(Settings,active=True)
        prefix = settings.prefix

    responsive = prefix.responsive
    source_dir = 'sync/' + responsive.source_dir
    response = SITE_ROOT + source_dir +'/Links/'+ placed_file

#   source_dir = os.path.abspath(os.path.dirname(__file__)+'/../') + '/' + source_dir
    source_dir = os.path.abspath(os.path.dirname(__name__)) + '/' + source_dir
    source_dir += '/Links/' + placed_file
    bits = placed_file.split('.')
    type = bits[-1].lower()
    if type != 'png' and type != 'gif':
        type = 'jpg'
    image_data = open(source_dir, "rb").read()
    return HttpResponse(image_data, content_type='image/' + type)

def LinksViewHome(request, placed_file):
    settings = get_object_or_404(Settings,active=True)
    path1 = settings.prefix.path
    response = LinksView(request, path1, placed_file)
    return response

#———————————————————————————————————————— send mail

from modules import send_mail

def MailView(request, lng):
    if request.method != 'POST': return HttpResponse(0)

    ua = request.META['HTTP_USER_AGENT']

    pfix = get_object_or_404(Prefix, path=lng)
    lng = pfix.language

    settings = get_object_or_404(Settings,active=True)
    response = send_mail.send(settings, lng, request.POST, ua)

    return HttpResponse(response)

#———————————————————————————————————————— 404 error
# https://websiteadvantage.com.au/404-Error-Handler-Checker

# Links folder redirection breaks if the prefix does not exist
# instead of defaulting to en, need to get site default language

@never_cache
def error404(request, *args, **kwargs):
    path1 = request.path.split('/')[1]

    try:
        prefix = Prefix.objects.get(path=path1)
    except ObjectDoesNotExist:
        settings = get_object_or_404(Settings,active=True)
        path1 = settings.prefix.path

    response = PageView(request, path1, 'missing',)
    response.status_code = 404
    return response

#———————————————————————————————————————— per-user cache
# https://gist.github.com/caot/6480c39453f5d2fa86bf

from django.core.cache import cache as core_cache

def cache_key(request):
    q = getattr(request, request.method)
    q.lists()
    urlencode = q.urlencode(safe='()')

    return 'pageview_%s_%s' % (request.path, urlencode)

def cache_per_user_function(ttl=None, cache_post=False):
    '''
    Decorator which caches the view for each User
    * ttl - the cache lifetime, do not send this parameter means that the cache
      will last until the restart server or decide to remove it
    * cache_post - Determine whether to make requests cache POST
    * The caching for anonymous users is shared with everyone
    
    How to use it:
    @cache_per_user_function(ttl=3600, cache_post=False)
    def my_view(request):
        return HttpResponse("LOL %s" % (request.user))
    '''
    def decorator(function):
        def apply_cache(request, *args, **kwargs):
            CACHE_KEY = cache_key(request)
            can_cache = True
            response = None

            if not cache_post and request.method == 'POST':
                can_cache = False

            if request.user.is_superuser:
                can_cache = False

            settings = get_object_or_404(Settings,active=True)
            if settings.cache_reset:
                can_cache = False
                settings.cache_reset = False
                settings.save()
            elif settings.cached: # cached even for superusers
                can_cache = True

            if can_cache:
                response = core_cache.get(CACHE_KEY, None)

            if not response:
                response = function(request, *args, **kwargs)
                if can_cache:
                    core_cache.set(CACHE_KEY, response, ttl)

            return response

        return apply_cache
    return decorator

#———————————————————————————————————————— page (with embedded svg)

from modules import svg_cleaner, meta_canonical, accessibility_links
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import redirect
from svija.models import Font

@cache_per_user_function(ttl=60*60*24, cache_post=False)
def PageView(request, path1, path2):

    #———————————————————————————————————————— check fer redirect

    try:
        redirect_obj = Redirect.objects.get(from_url=request.path, active=True)
        if redirect_obj.to_prefix[0:4] == 'http':
            return HttpResponseRedirect(redirect_obj.to_prefix + '://' + redirect_obj.to_page)
        else:
            return HttpResponseRedirect('/'+redirect_obj.to_prefix + '/' + redirect_obj.to_page)
    except ObjectDoesNotExist:
        rien = 0

    #———————————————————————————————————————— load objects

    prefix     = get_object_or_404(Prefix, path=path1)
    page       = get_object_or_404(Page, Q(prefix__path=path1) & Q(url=path2) & Q(visitable=True))
    responsive = get_object_or_404(Responsive, name=prefix.responsive.name)
    settings   = get_object_or_404(Settings,active=True)
    language   = prefix.language

    #———————————————————————————————————————— if /en/ or /en/home then redirect to /

    part_path = '/' + settings.prefix.path +'/'
    full_path = part_path + settings.prefix.default

    if request.path == full_path or request.path == part_path:
        response = redirect('/')
        response.status_code = 301
        return response

    #———————————————————————————————————————— if /fr/accueil then redirect to /fr/

    part_path = '/' + path1 +'/'
    full_path = part_path + prefix.default

    if request.path == full_path:
        response = redirect(part_path)
        response.status_code = 301
        return response

    #———————————————————————————————————————— context for template

    comments      = ''
    title         = ''
    meta          = ''
    fonts         = ''
    touch         = ''
    head_js       = ''
    head_css      = ''
    accessibility = ''
    svg           = ''
    html          = ''
    form          = ''
    menu          = ''
    analytics_id  = ''
    body_js       = ''

    #———————————————————————————————————————— the easy ones

    comments     = language.comment
    title        = page.title + ' ' + language.title
    touch        = language.touch
    analytics_id = settings.analytics_id

    #———————————————————————————————————————— meta tag

    # just send necessary parts, not whole objects
    meta  = meta_canonical.create_canonical(
        prefix,
        responsive,
        language,
        settings.url,
        path1,
        path2,
    )

    #———————————————————————————————————————— fonts
    # should be first in CSS

    font_objs = Font.objects.all()
    css_str  = "@font-face {{ font-family:'{}'; src:url('{}'){}; }}"
    link_str = '\n  <link rel="stylesheet" href="{}" />'
    css_final = ''
    link_final = ''
    google_fonts = []

    for this_font in font_objs:
        if this_font.active:
            font_face = this_font.name
            font_src  = this_font.source

            if this_font.google:
                req = this_font.style.lower().replace(' ','')
                req = this_font.family.replace(' ','+') + ':' + req 
                google_fonts.append(req)

            elif font_src.find('woff2') > 0:
                font_format = " format('woff2')"
                font_src = '/fonts/' + font_src
                css_final  += '\n'+ css_str.format(font_face, font_src, font_format)

            elif font_src.find('woff') > 0:  
                font_format = " format('woff')"
                font_src = '/fonts/' + font_src
                css_final += '\n'+ css_str.format(font_face, font_src, font_format)

    head_css = css_final + head_css

    link_str = '<link rel="stylesheet" href="https://fonts.googleapis.com/css?family={}">'
    fonts = link_str.format(('|').join(google_fonts))

    #———————————————————————————————————————— head JS

    dim_js = ''

    if settings.secure:
        page_url = 'https://'
    else:
        page_url = 'http://'

    page_url += settings.url + '/' + path1 + '/' + path2
    head_js += "var page_url = '" + page_url + "';\n"

    if page.override:
        dim_js += '// overridden in page settings:\n'

        dim_js += 'var page_width = '    + str(page.width  ) + '; '
        dim_js += 'var page_visible = '  + str(page.visible) + '; \n'
        dim_js += 'var page_offsetx = '  + str(page.offsetx) + '; '
        dim_js += 'var page_offsety = '  + str(page.offsety) + '; \n'

    else:
        dim_js += 'var page_width = '    + str(responsive.width)   + '; '
        dim_js += 'var page_visible = '  + str(responsive.visible) + '; \n'
        dim_js += 'var page_offsetx = '  + str(responsive.offsetx) + '; '
        dim_js += 'var page_offsety = '  + str(responsive.offsety) + '; \n'

    head_js += dim_js

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

    shared = page.shared.sharedscripts_set.all()  

    for this_script in shared:
        if this_script.type == 'CSS' and this_script.active == True:
            head_css += '\n' + this_script.content

        if this_script.type == 'head JS' and this_script.active == True:
            head_js += '\n' + this_script.content

        if this_script.type == 'body JS' and this_script.active == True:
            body_js += '\n' + this_script.content

    #———————————————————————————————————————— accessiblity/seo

    text = page.access_text
    links = accessibility_links.create(settings.url, Page.objects.all())
    capture = '/images/capture.jpg'

    tag = '{0}\n\n{1}<a href=http://{2}><img src={3} style="width:80%;height:2rem"></a>'
    accessibility = tag.format(text,links,settings.url,capture)

    #———————————————————————————————————————— svg

    source_dir = 'sync/' + responsive.source_dir

    if page.override:
        final_width = page.width
    else:
        final_width = responsive.width

    all_svgs  = page.svg_set.all()
    svg = ''

    for this_svg in all_svgs:
        if this_svg.active:

            #—————— check if svg exists
            temp_source = os.path.abspath(os.path.dirname(__name__)) + '/' + source_dir + '/' + this_svg.filename
            path = pathlib.Path(temp_source)
            if not path.exists():
                return error404(request)

            svg_ID, px_width, px_height, svg_content = svg_cleaner.clean(temp_source, this_svg.filename)
    
            page_ratio = px_width/px_height # 1680/2600=0.6461538462
    
            rem_width = final_width/10
            rem_height = final_width/page_ratio/10
    
            css_dims = '#' + svg_ID + '{ width:' + str(rem_width) + 'rem; height:' + str(rem_height) + 'rem; }'
            head_css += '\n\n' + css_dims
            svg += '\n' + svg_content

    #———————————————————————————————————————— page scripts

    html     = ''
    form     = ''

    all_scripts = page.pagescripts_set.all()

    for this_script in all_scripts:
        if this_script.type == 'head JS' and this_script.active == True:
            head_js += '\n' + this_script.content

        if this_script.type == 'body JS' and this_script.active == True:
            body_js += '\n' + this_script.content

        if this_script.type == 'CSS' and this_script.active == True:
            head_css += '\n' + this_script.content

        if this_script.type == 'HTML' and this_script.active == True:
            html += '\n' + this_script.content

        if this_script.type == 'form' and this_script.active == True:
            form += '\n' + this_script.content

    if form != '': head_js += form_js

    #———————————————————————————————————————— library scripts

#   html     = ''
#   form     = ''

    all_scripts = page.library_script.all()

    for this_script in all_scripts:
        if this_script.type == 'head JS':
            head_js += '\n' + this_script.content

        if this_script.type == 'body JS':
            body_js += '\n' + this_script.content

        if this_script.type == 'CSS':
            head_css += '\n' + this_script.content

        if this_script.type == 'HTML':
            html += '\n' + this_script.content

        if this_script.type == 'form':
            form += '\n' + this_script.content

    #———————————————————————————————————————— menu

    all_svgs = page.menu.all()
    menu = ''

    for this_svg in all_svgs:

        #—————— check if svg exists
        temp_source = os.path.abspath(os.path.dirname(__name__)) + '/' + source_dir + '/' + this_svg.filename
        path = pathlib.Path(temp_source)
        if not path.exists():
            return error404(request)

        svg_ID, px_width, px_height, svg_content = svg_cleaner.clean(temp_source, this_svg.filename)
        css_dims = '#' + svg_ID + '{ width:' + str(px_width/10) + 'rem; height:' + str(px_height/10) + 'rem; }'

        head_css += '\n\n' + css_dims
        menu += '\n' + svg_content

        all_scripts = this_svg.menuscripts_set.all()
        for this_script in all_scripts:
            if this_script.type == 'CSS' and this_script.active == True:
                head_css += '\n' + this_script.content
            if this_script.type == 'head JS' and this_script.active == True:
                head_js += '\n' + this_script.content
            if this_script.type == 'body JS' and this_script.active == True:
                body_js += '\n' + this_script.content

#   #———————————————————————————————————————— old cache clearing-scheme

#   if request.GET.get('clear') == 'cache':
#       if request.user.is_superuser:
#           title = request.GET.get('flag') + ' - ' + title 
#           cache.clear()

    #———————————————————————————————————————— page settings

    template = page.template.filename

    if form != '':
        template = template.replace('.html', '_token.html')

    # set it up
    context = {
        'comments'      : comments,
        'title'         : title,
        'meta'          : meta,
        'fonts'         : fonts,
        'touch'         : touch,
        'head_js'       : head_js,
        'css'           : head_css,
        'accessibility' : accessibility,
        'svg'           : svg,
        'html'          : html,
        'form'          : form,
        'menu'          : menu,
        'analytics_id'  : analytics_id,
        'body_js'       : body_js
    }

    return render(request, template, context)
#   return render(request, template, {'context':context})

#———————————————————————————————————————— fin
