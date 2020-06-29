#———————————————————————————————————————— attribute_scripts.py

from modules.add_script import *
from PageView import page_obj

def attribute_scripts(label, script_list, svg_passthrough, css_dimensions):

    css      = '\n\n/*———————————————————————————————————————— '    + label + ' scripts */\n\n'
    head_js  = '\n\n//———————————————————————————————————————— '    + label + ' scripts\n\n'
    body_js  = '\n\n//———————————————————————————————————————— '    + label + ' scripts\n\n'
    html     = '\n\n<!-- ———————————————————————————————————————— ' + label + ' scripts -->\n\n'
    form     = '\n\n<!-- ———————————————————————————————————————— ' + label + ' scripts -->\n\n'

    css += css_dimensions

    for this_script in script_list:
        if this_script.type == 'CSS' and this_script.active == True:
            css += add_script('css', this_script.name, this_script.content)

        if this_script.type == 'head JS' and this_script.active == True:
            head_js += add_script('js', this_script.name, this_script.content)

        if this_script.type == 'body JS' and this_script.active == True:
            body_js += add_script('js', this_script.name, this_script.content)

        if this_script.type == 'HTML' and this_script.active == True:
            html += add_script('html', this_script.name, this_script.content)

        if this_script.type == 'form' and this_script.active == True:
            form += add_script('html', this_script.name, this_script.content)

    results = page_obj(head_js, css, body_js, svg_passthrough, html, form)
    return results
