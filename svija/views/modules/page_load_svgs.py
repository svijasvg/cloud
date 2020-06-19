
#———————————————————————————————————————— load all SVG's on a page

from modules import svg_cleaner
from modules.get_single_svg import *

def page_load_svgs(all_svgs, source_dir, specified_width, use_p3):
    
    head_css = svg = ''

    for this_svg in all_svgs: #WHERE ACTIVE == TRUE, ORDER BY LOAD_ORDER
        if this_svg.active:
            s, c = get_single_svg(this_svg, source_dir, specified_width, use_p3)
            svg += s
            head_css += c

    results = {
        'head_css': head_css,
        'svg'     : svg,
    }
    return results

