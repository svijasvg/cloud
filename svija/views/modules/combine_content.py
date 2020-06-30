#———————————————————————————————————————— views/modules/combine_content.py

# accepts a list of content blocks that each contain 6 elements

from modules.svg_cleaner import *
from modules.get_single_svg import *
from PageView import page_obj

def combine_content(blocks):

    js = css = body = ''

    for i in blocks:
        js   += i['head_js']
        css  += i['css']
        body += i['svgs']
        body += i['html']
        body += i['form']
        body += '<script>' + i['body_js'] + '</script>'

    return { 'js':js, 'css':css, 'body':body, }
