#———————————————————————————————————————— views/modules/combine_content.py

# accepts a list of content blocks that each contain 6 elements

from modules.svg_cleaner import *
from modules.get_single_svg import *
from modules.add_script import *
from PageView import page_obj

def combine_content(content_blocks):

    head_js = css =  body_js = svgs = html = form = ''

    for i in content_blocks:
        head_js += i['head_js']
        css     += i['css']
        body_js += i['body_js']
        html    += i['svgs']
        html    += i['html']
        html    += i['form']

    combined_content = {
        'js':'', 'css':'', 'body':'', }

    combined_content['js']    = head_js
    combined_content['css']   = css
    combined_content['body']  = html + '<script>' + body_js + '</script>'

    return combined_content
