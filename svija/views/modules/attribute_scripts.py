#———————————————————————————————————————— attribute_scripts.py

from modules.add_script import *
from PageView import page_obj

#ef attribute_scripts(core_content, label, sitewide):
def attribute_scripts(label, sitewide):

    css      = '\n\n/*———————————————————————————————————————— '    + label + ' scripts */\n\n'
    head_js  = '\n\n//———————————————————————————————————————— '    + label + ' scripts\n\n'
    body_js  = '\n\n//———————————————————————————————————————— '    + label + ' scripts\n\n'
    html     = '\n\n<!-- ———————————————————————————————————————— ' + label + ' scripts -->\n\n'
    form     = '\n\n<!-- ———————————————————————————————————————— ' + label + ' scripts -->\n\n'

    for this_script in sitewide:
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

    results = page_obj(head_js, css, body_js, '', html, form)
    return results
