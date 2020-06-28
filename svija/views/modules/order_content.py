#———————————————————————————————————————— views/modules/order_content.py

# accepts a list of modules, some inactive
# a module has exactly 1 svg filename, and it can be empty

from modules.svg_cleaner import *
from modules.get_single_svg import *
from modules.add_script import *
from PageView import page_obj

def order_content(module_list):
    ordered_content = {
        'meta_fonts':'', 'head_js':'', 'css':'', 'body_js':'', 'svgs':'', 'html':'', }

# meta_fonts
# head_js
# css
# body_js
# svgs
# html
# form

    meta_fonts = head_js = css =  body_js = svgs = html = form = ''

#   for this_module in module_list:
#       if 'meta_fonts' in this_module:
#            rien = 0
#           meta_fonts += this_module['meta_fonts']

    ordered_content['meta_fonts'] += meta_fonts
    ordered_content['head_js']    += head_js
    ordered_content['css']        += css
    ordered_content['body_js']    += body_js
    ordered_content['svgs']       += svgs
    ordered_content['html']       += html

    return ordered_content
