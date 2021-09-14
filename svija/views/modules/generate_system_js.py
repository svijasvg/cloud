#———————————————————————————————————————— views/modules/generate_system_js.py

#———————————————————————————————————————— imports

from svija.models import Prefix, Responsive

#     need current language code
#     all prefixes where language=language code
#     for eady prefix,
#     
#     fr = fr['desktop'], fm['mobile']


def generate_system_js(version, language, settings, page, request_prefix, request_slug, responsive, screens):

    system_js = "//———————————————————————————————————————— system js\n\n"
    
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

    all_screens = []
    for screen in screens:
        all_screens.append( "'" + screen.code + "':'" + str(screen.limit) + "'")

    system_js += "var screens = {" + ', '.join(all_screens) + "};\n" 

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
