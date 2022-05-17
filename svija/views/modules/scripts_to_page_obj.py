#———————————————————————————————————————— scripts_to_page_obj.py

#———————————————————————————————————————— imports

from modules.get_script import *
from PageObject import page_obj

#———————————————————————————————————————— def scripts_to_page_obj(label, script_list, svg_passthrough, css_dimensions):

def scripts_to_page_obj(label, script_list, svg_passthrough, css_dimensions):

    label = '———————————————————————————————————————— ' + label + ' scripts'

    comm_head_js = comm_css = comm_body_js = comm_html = comm_form = ''
    head_js = css = body_js = html = form = ''

    css += css_dimensions

    for this_script in script_list:
        if this_script.type == 'head JS' and this_script.active == True:
            comm_head_js = '\n\n//' + label + '\n\n'
            head_js += get_script('js', this_script.name, this_script.content)

        if this_script.type == 'CSS' and this_script.active == True:
            comm_css = '\n\n/*' + label + ' */\n\n'
            css += get_script('css', this_script.name, this_script.content)

        if this_script.type == 'body JS' and this_script.active == True:
            comm_body_js = '\n\n//' + label + '\n\n'
            body_js += get_script('js', this_script.name, this_script.content)

        if this_script.type == 'HTML' and this_script.active == True:
            comm_html = '\n\n<!-- ' + label + ' -->\n\n'
            html += get_script('html', this_script.name, this_script.content)

        if this_script.type == 'form' and this_script.active == True:
            comm_form = '\n\n<!-- ' + label + ' -->\n\n'
            form += get_script('html', this_script.name, this_script.content)

    head_js = comm_head_js + head_js
    css = comm_css + css
    body_js = comm_body_js + body_js
    html = comm_html + html
    form = comm_form + form

    # form closing tag is included in csrf token template
    # form = form.replace('</form>', '')

    return page_obj(head_js, css, body_js, svg_passthrough, html, form)
