#———————————————————————————————————————— get_page_svgs.py
#———————————————————————————————————————— comments

#   also supplies CSS for initial_scroll div

#———————————————————————————————————————— import

from modules.get_single_svg import *

#———————————————————————————————————————— def

def get_page_svgs(screen_code, page, page_width, use_p3):

    svgs = ''
    scrollDiv = ''

    all_svgs  = page.illustrator_fk.filter(enabled=True).order_by('zindex')

    css = svgs = ''

    # also edit modules/generate_system_js.py
    for this_svg in all_svgs:
        if this_svg.enabled:
            s, c, d = get_single_svg(this_svg, screen_code, page_width, use_p3, True)
            svgs += s
            css += c
            
            if scrollDiv == '':
              scrollDiv = d

    return svgs, scrollDiv+css

#———————————————————————————————————————— fin
