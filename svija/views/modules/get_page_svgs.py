#———————————————————————————————————————— get_page_svgs.py

from modules import svg_cleaner
from modules.get_single_svg import *

def get_page_svgs(page, source_dir, specified_width, use_p3):

    svgs = ''
    all_svgs  = page.svg_set.all()

    css = svgs = ''

    for this_svg in all_svgs: #WHERE ACTIVE == TRUE, ORDER BY LOAD_ORDER
        if this_svg.active:
            s, c = get_single_svg(this_svg, source_dir, specified_width, use_p3)
            svgs += s
            css += c

    return svgs, css
