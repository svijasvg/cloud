#———————————————————————————————————————— views/modules/generate_system_js.py

from svija.models import Prefix, Responsive

#     need current language code
#     all prefixes where language=language code
#     for eady prefix,
#     
#     fr = fr['desktop'], fm['mobile']

def generate_system_js(version, language, settings, page, request_prefix, request_slug, responsive):

    system_js = "//———————————————————————————————————————— view module generate_system_js\n\n"
    
#———————————————————————————————————————— easy ones

    # version information
    system_js += "var svija_version='" + version + "';\n"

    # language information
    system_js += 'var page_key = "' + str(page.pk) +'";\n'

    # language information
    system_js += 'var language_code = "' + language.code +'";\n'

    # responsive information
    system_js += 'var responsive_code = "' + responsive.code +'";\n'

#———————————————————————————————————————— screens

    # all prefixes for this language
    prefix_list = list(Prefix.objects.filter(language = language.pk))

    all_resps = []
    for prf in prefix_list: 
        resp = prf.responsive
        resp_name = resp.name
#       scpt += "'" + resp_name + "':'" + pfix.path + "'"
        all_resps.append( "'" + resp_name + "':'" + prf.path + "'")

    system_js += "var responsives = {" + ', '.join(all_resps) + "};\n"

#———————————————————————————————————————— .ai urls

# this is so the image algorithm can find the correct images.
# there should not be two different images with the same name
# it will not be an issue once images are optimized in a single directory

# could start by copying all images to a special directory, with no optimization

# for now, the paths will give a set of clues where an image could be
# but they will not necessarily be available to the image loader
# we'll see when the cookie data is available

    svg_list = []
    all_svgs  = page.svg_set.all()

    for this_svg in all_svgs: #WHERE ACTIVE == TRUE, ORDER BY LOAD_ORDER
        if this_svg.active:
            svg_list.append(this_svg.filename)

    system_js += "var ai_files  = [\"" + '",\n"'.join(svg_list) + "\"];\n"

#———————————————————————————————————————— data

    # accept cookies by default
    if settings.tracking_on: system_js += "var tracking_on = true;\n"
    else:                    system_js += "var tracking_on = false;\n"

    # page url
    if settings.secure: page_url = 'https://'
    else:               page_url = 'http://'

    page_url += settings.url + '/' + request_prefix + '/' + request_slug

    system_js += "var page_url = '" + page_url + "';\n"

#———————————————————————————————————————— page dimension information

    dim_js = ''

    if page.override_dims:
        dim_js += '\n// overridden in page settings:\n'

        dim_js += 'var page_width = '     + str(page.width  ) + ';\n'
        dim_js += 'var visible_width = '  + str(page.visible) + ';\n'
        dim_js += 'var page_offsetx = '   + str(page.offsetx) + ';\n'
        dim_js += 'var page_offsety = '   + str(page.offsety) + ';\n'

    else:
        dim_js += 'var page_width = '     + str(responsive.width)   + ';\n'
        dim_js += 'var visible_width = '  + str(responsive.visible) + ';\n'
        dim_js += 'var page_offsetx = '   + str(responsive.offsetx) + ';\n'
        dim_js += 'var page_offsety = '   + str(responsive.offsety) + ';\n'

    system_js += dim_js

#———————————————————————————————————————— unused scrolling

# get scroll position too
#   override_dims = models.BooleanField(default=False, verbose_name='override dimensions',)
#   width = models.PositiveSmallIntegerField(default=0, verbose_name='page width in pixels')
#   visible = models.PositiveSmallIntegerField(default=0, verbose_name='visible width in pixels')
#   offsetx = models.PositiveSmallIntegerField(default=0, verbose_name='offset x in pixels')
#   offsety = models.PositiveSmallIntegerField(default=0, verbose_name='offset y in pixels')
    
    return system_js

#———————————————————————————————————————— fin
