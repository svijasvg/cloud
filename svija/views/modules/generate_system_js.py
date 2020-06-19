    #———————————————————————————————————————— views.py generated JS

def generate_system_js(version, language, settings, page, request_prefix, request_slug, responsive):

    # version information
    system_js = "var svija_version='" + version + "';\n"

    # language information
    cde = language.code
    system_js += 'var language_code = "' + cde +'";\n'

    # accept cookies by default
    if settings.tracking_on: system_js += "var tracking_on = true;\n"
    else:                    system_js += "var tracking_on = false;\n"

    # page url
    if settings.secure: page_url = 'https://'
    else:               page_url = 'http://'

    page_url += settings.url + '/' + request_prefix + '/' + request_slug
    system_js += "var page_url = '" + page_url + "';\n"

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

    system_js += dim_js

    return system_js
