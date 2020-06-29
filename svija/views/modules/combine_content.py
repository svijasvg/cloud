#———————————————————————————————————————— views/modules/combine_content.py

# accepts a list of content blocks that each contain 6 elements

from modules.svg_cleaner import *
from modules.get_single_svg import *
from modules.add_script import *
from PageView import page_obj

def combine_content(content_blocks):

    combined_content = {
        'head_js':'', 'css':'', 'body_js':'', 'svgs':'', 'html':'', }

    head_js = css =  body_js = svgs = html = form = ''

    head_js    += ''.join([i['head_js']    for i in content_blocks])
    css        += ''.join([i['css']        for i in content_blocks])
    body_js    += ''.join([i['body_js']    for i in content_blocks])
    svgs       += ''.join([i['svgs']       for i in content_blocks])
    html       += ''.join([i['html']       for i in content_blocks])
    html       += ''.join([i['form']       for i in content_blocks])

    combined_content['head_js']    += head_js
    combined_content['css']        += css
    combined_content['body_js']    += body_js
    combined_content['svgs']       += svgs
    combined_content['html']       += html

    return combined_content
