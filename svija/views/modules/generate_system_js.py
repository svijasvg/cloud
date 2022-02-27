#———————————————————————————————————————— views/modules/generate_system_js.py

#———————————————————————————————————————— notes
#
#
#
#
#
#———————————————————————————————————————— imports

from svija.models import Screen

#     need current language code
#     all prefixes where language=language code
#     for eady prefix,
#     
#     fr = fr['desktop'], fm['mobile']


def generate_system_js(version, settings, page, language_code, request_slug, this_screen, screens):

#   this_screen = Screen.objects.filter(code=screen).first()

    system_js = "//———————————————————————————————————————— system js\n\n"
    
#———————————————————————————————————————— easy ones

    # version information
    system_js += "var svija_version='" + version + "';\n"

    # language information
    system_js += 'var language_code = "' + language_code +'";\n'

    # responsive information
    system_js += 'var screen_code = "' + this_screen.code +'";\n'

#———————————————————————————————————————— screens

    all_x_screens = []
    for one_screen in screens:
        all_x_screens.append( str(one_screen.limit) +  ', "' + one_screen.code +'"')

    system_js += "var all_screens = [[" + '], ['.join(all_x_screens) + "]];\n" 

#———————————————————————————————————————— data

    # accept cookies by default
    if settings.tracking_on: system_js += "var tracking_on = true;\n"
    else:                    system_js += "var tracking_on = false;\n"

    page_url = 'https://'
    page_url += settings.url + '/' + language_code + '/' + request_slug

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
        dim_js += 'var page_width = '     + str(this_screen.width)   + ';\n'
        dim_js += 'var visible_width = '  + str(this_screen.visible) + ';\n'
        dim_js += 'var page_offsetx = '   + str(this_screen.offsetx) + ';\n'
        dim_js += 'var page_offsety = '   + str(this_screen.offsety) + ';\n'

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
