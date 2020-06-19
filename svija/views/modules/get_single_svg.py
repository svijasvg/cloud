
#———————————————————————————————————————— get 1 SVG & calculate sizes

import os
import pathlib
from modules.svg_cleaner import *

def get_single_svg(this_svg, source_dir, specified_width, use_p3):

    css = svg = ''

    # can be empty if it's a module that doesn't include an SVG
    if this_svg.filename != '':

        #—————— check if svg exists
        temp_source = os.path.abspath(os.path.dirname(__name__)) + '/' + source_dir + '/' + this_svg.filename
        path = pathlib.Path(temp_source)

        if not path.exists():
            svg = '<!-- missing svg: {} -->'.format(this_svg.filename)
 
        else:
            svg_ID, svg_width, svg_height, svg_content = clean(temp_source, this_svg.filename, use_p3)
 
            if svg_width > specified_width:
                page_ratio = svg_height/svg_width
                svg_width = specified_width
                svg_height = round(specified_width * page_ratio)
 
            rem_width = svg_width/10
            rem_height = svg_height/10
 
            css_dims = '#' + svg_ID + '{ width:' + str(rem_width) + 'rem; height:' + str(rem_height) + 'rem; }'
            css += '\n\n' + css_dims
            svg += '\n' + svg_content
 
    return svg, css

