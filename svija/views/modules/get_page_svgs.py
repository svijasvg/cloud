#———————————————————————————————————————— get_page_svgs.py

from modules import svg_cleaner
from modules.get_single_svg import *

def get_page_svgs(screen_code, page, page_width, use_p3):

    svgs = ''
    all_svgs  = page.svg_set.all()

    css = svgs = ''

    # also edit modules/generate_system_js.py
    for this_svg in all_svgs: #WHERE ACTIVE == TRUE, ORDER BY LOAD_ORDER
        if this_svg.active:
            s, c = get_single_svg(this_svg, screen_code, page_width, use_p3)
            svgs += s
            css += c

    return svgs, css
