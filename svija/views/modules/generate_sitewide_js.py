#———————————————————————————————————————— generate_sitewide_scripts.py

from modules.add_script import *

def generate_sitewide_js(sitewide):

    head_css = '\n//———————————————————————————————————————— sitewide scripts\n'
    head_js  = '\n//———————————————————————————————————————— sitewide scripts\n'
    body_js  = '\n//———————————————————————————————————————— sitewide scripts\n'

    for this_script in sitewide:
        if this_script.type == 'CSS' and this_script.active == True:
            head_css += add_script('css', this_script.name, this_script.content)

        if this_script.type == 'head JS' and this_script.active == True:
            head_js += add_script('js', this_script.name, this_script.content)

        if this_script.type == 'body JS' and this_script.active == True:
            body_js += add_script('js', this_script.name, this_script.content)

    return head_css, head_js, body_js
