#———————————————————————————————————————— views/modules/order_content.py

# accepts a list of content blocks that each contain 6 elements

from modules.svg_cleaner import *
from modules.get_single_svg import *
from modules.add_script import *
from PageView import page_obj

def order_content(module_list):

    ordered_content = {
        'head_js':'', 'css':'', 'body_js':'', 'svgs':'', 'html':'', }

    head_js = css =  body_js = svgs = html = form = ''

    head_js    += ''.join([i['head_js']    for i in module_list])
    css        += ''.join([i['css']        for i in module_list])
    body_js    += ''.join([i['body_js']    for i in module_list])
    svgs       += ''.join([i['svgs']       for i in module_list])
    html       += ''.join([i['html']       for i in module_list])
    html       += ''.join([i['form']       for i in module_list])

    ordered_content['head_js']    += head_js
    ordered_content['css']        += css
    ordered_content['body_js']    += body_js
    ordered_content['svgs']       += svgs
    ordered_content['html']       += html

    return ordered_content
