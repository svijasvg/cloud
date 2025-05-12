
#:::::::::::::::::::::::::::::::::::::::: views/modules/generate_system_js.py

#———————————————————————————————————————— notes
#
#
#
#
#
#———————————————————————————————————————— imports

import re
import time
from svija.models import Screen

#     need current section code
#     all prefixes where section=section code
#     for eady prefix,
#     
#     fr = fr['desktop'], fm['mobile']


#:::::::::::::::::::::::::::::::::::::::: definition

def generate_system_js(user, version, settings, page, section_code, request_slug, this_screen, screens):

#   this_screen = Screen.objects.filter(code=screen).first()

    system_js = "//———————————————————————————————————————— system js\n\n"
    
#———————————————————————————————————————— easy ones

    # version information
    system_js += "var svija_version='" + version + "'\n"

    # section information
    system_js += 'var section_code = "' + section_code +'"\n'

    # responsive information
    system_js += 'var screen_code = "' + this_screen.code +'"\n'

    # responsive information
    system_js += 'var page_pk = ' + str(page.id) +'\n'

    # milliseconds
    system_js += 'var milliseconds = "' + str(time.time_ns()) +'"\n'

#———————————————————————————————————————— screens

    all_x_screens = []
    # page.pagescript_set.filter(enabled=True).order_by('order')
    for one_screen in screens:
      if one_screen.code != '★':
        all_x_screens.append( str(one_screen.pixels) +  ', "' + one_screen.code +'"' +  ', "' + one_screen.name +'"')

    system_js += "var all_screens = [[" + '], ['.join(all_x_screens) + "]]\n" 

#———————————————————————————————————————— data

    # accept cookies by default
    if settings.tracking_on: system_js += "var tracking_on = true\n"
    else:                    system_js += "var tracking_on = false\n"

    page_url = 'https://'
    page_url += settings.url + '/' + section_code + '/' + request_slug

    system_js += "var page_url = '" + page_url + "'\n"

#———————————————————————————————————————— admin signed in?

    # doesn't work in Chrome

    if user.is_superuser:
      system_js += "var admin=true\n"

#———————————————————————————————————————— page dimension information

    dim_js = ''

    if not page.default_dims:
        dim_js += '\n// overridden in page settings:\n'

        dim_js += 'var page_width = '     + str(page.width  ) + '\n'
        dim_js += 'var visible_width = '  + str(page.visible) + '\n'
        dim_js += 'var page_offsetx = '   + str(page.offsetx) + '\n'
        dim_js += 'var page_offsety = '   + str(page.offsety) + '\n'

    else:
        dim_js += 'var page_width = '     + str(this_screen.width)   + '\n'
        dim_js += 'var visible_width = '  + str(this_screen.visible) + '\n'
        dim_js += 'var page_offsetx = '   + str(this_screen.offsetx) + '\n'
        dim_js += 'var page_offsety = '   + str(this_screen.offsety) + '\n'

    system_js += dim_js

    return system_js


#:::::::::::::::::::::::::::::::::::::::: fin
