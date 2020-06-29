#———————————————————————————————————————— attribute_scripts.py

from modules.add_script import *

#ef attribute_scripts(core_content, label, sitewide):
def attribute_scripts(label, sitewide):

    head_css = '\n\n/*———————————————————————————————————————— ' + label + ' scripts */\n\n'
    head_js  = '\n\n//———————————————————————————————————————— ' + label + ' scripts\n\n'
    body_js  = '\n\n//———————————————————————————————————————— ' + label + ' scripts\n\n'
    html     = '\n\n<!-- ———————————————————————————————————————— ' + label + ' scripts -->\n\n'
    form     = '\n\n<!-- ———————————————————————————————————————— ' + label + ' scripts -->\n\n'

    for this_script in sitewide:
        if this_script.type == 'CSS' and this_script.active == True:
            head_css += add_script('css', this_script.name, this_script.content)

        if this_script.type == 'head JS' and this_script.active == True:
            head_js += add_script('js', this_script.name, this_script.content)

        if this_script.type == 'body JS' and this_script.active == True:
            body_js += add_script('js', this_script.name, this_script.content)

        if this_script.type == 'HTML' and this_script.active == True:
            html += add_script('html', this_script.name, this_script.content)

        if this_script.type == 'form' and this_script.active == True:
            form += add_script('html', this_script.name, this_script.content)

    return head_css, head_js, body_js, html, form

#   core_content['head_js'] += head_js
#   core_content['css']     += head_css
#   core_content['body_js'] += body_js
#   core_content['html']    += html
#   core_content['form']    += form

#   return core_content
