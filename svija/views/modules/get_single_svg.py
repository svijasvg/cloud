
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
            is_module = hasattr(this_svg, 'css_id')

            temp_id = this_svg.filename
            if is_module:
                if this_svg.css_id != '':
                    temp_id = this_svg.css_id

            svg_ID, svg_width, svg_height, svg_content = clean(temp_source, temp_id, use_p3)
 
            if svg_width > specified_width:
                page_ratio = svg_height/svg_width
                svg_width = specified_width
                svg_height = round(specified_width * page_ratio)
 
            rem_width  = round(svg_width/10,  3)
            rem_height = round(svg_height/10, 3)
 
            if is_module:
                css_dims = '#' + svg_ID + '{\n'
                css_dims += 'width:' + str(rem_width) + 'rem; height:' + str(rem_height) + 'rem; '
                y = calculate_css(this_svg)
                css += '\n\n' + css_dims + '\n' + y + '\n' + '}'
            else:
                css_dims = '#' + svg_ID + '{ width:' + str(rem_width) + 'rem; height:' + str(rem_height) + 'rem; }'
                css += '\n\n' + css_dims

            svg += '\n' + svg_content
 
    return svg, css

def calculate_css(this_svg):
    posit  = dic_position(this_svg.position)
    offset = dic_corners(this_svg.corner, this_svg.position)
    xoff = str(this_svg.horz_offset/10) + 'rem'
    yoff = str(this_svg.vert_offset/10) + 'rem'
    offset = offset.replace('xrem', xoff)
    offset = offset.replace('yrem', yoff)
    return posit + offset
  
def dic_position(pos):
    if pos != 'absolute' and pos != 'floating' and pos != '': return '/* invalid svg position */'
    return {
        'absolute': 'position: absolute;\n',
        'floating': 'position: fixed;\n',
        ''        : '',
    }[pos]

def dic_corners(cor, pos):
    if pos != 'absolute' and pos != 'floating' and pos != '': return '/* invalid svg position */'
    if pos ==  '': return ''
    return {
        'top left'    : 'left: xrem; right: ; top: yrem; bottom: ;\n',
        'top right'   : 'left: ; right: xrem; top: yrem; bottom: ;\n',
        'bottom right': 'left: ; right: xrem; top: ; bottom: yrem;\n',
        'bottom left' : 'left: xrem; right: ; top: ; bottom: yrem;\n',
    }[cor]


#   positions = ('absolute', 'floating', 'bottom',)
#   corners = ('top left', 'top right', 'bottom left', 'bottom right',)

#   css_id = models.CharField(max_length=200, default='', verbose_name='object ID',)
#   position = models.CharField(max_length=255, default='absolute', choices=Choices(*positions), verbose_name='placement')
#   corner = models.CharField(max_length=255, default='top left', choices=Choices(*corners), verbose_name='reference corner')
#   horz_offset = models.PositiveSmallIntegerField(default=0, verbose_name='horizontal offset (px)',)
#   vert_offset = models.PositiveSmallIntegerField(default=0, verbose_name='vertical offset (px)',)
