#———————————————————————————————————————— get_single_svg.py

#———————————————————————————————————————— import

import os
import pathlib
from modules.svg_cleaner import *

#———————————————————————————————————————— get_single_svg(target_obj, page_width, use_p3):

def get_single_svg(target_obj, screen_code, page_width, use_p3):

    css = svg = ''

    # can be empty if module without SVG
    if not hasattr(target_obj, 'filename'): return svg, css

    ai_name = target_obj.filename
    if ai_name == '':
      return svg, css


    # remove everything in beginning of path if necessary
    # /Users/Main/Library/Mobile Documents/com~apple~CloudDocs/sync/svija.dev/sync/test.ai

    if ai_name.find('/') > -1:
      ai_name = ai_name.rpartition("/")[2]
      target_obj.filename = ai_name
      target_obj.save()

    raw_name = ai_name[:-3]
    svg_name = raw_name + '_' + screen_code + '.svg'

    svija_path = '/sync/Svija/SVG Files/'
    abs_path = os.path.abspath(os.path.dirname(__name__))

    #—————— check if svg exists

    svg_path = abs_path + svija_path + svg_name

    path = pathlib.Path(svg_path)

    if not path.exists():
        #vg = '<!-- missing svg: {} -->'.format(target_obj.filename)
        svg = '<!-- missing svg: {} -->'.format(svg_path)

    else:
        is_module = hasattr(target_obj, 'css_id')

        temp_id = raw_name
        if is_module:
            if target_obj.css_id != '':
                temp_id = target_obj.css_id


        svg_ID, svg_width, svg_height, svg_content = clean(svg_path, temp_id, use_p3)
        svg = '<!-- ' + svg_ID + ', ' + str(svg_width) + ', ' + str(svg_height) + ' -->'

        if svg_width > page_width:
            page_ratio = svg_height/svg_width
            svg_width = page_width
            svg_height = round(page_width * page_ratio)

        rem_width  = round(svg_width/10,  3)
        rem_height = round(svg_height/10, 3)

        if is_module:
            css_dims = '#' + svg_ID + '{\n'
            css_dims += 'width:' + str(rem_width) + 'rem; height:' + str(rem_height) + 'rem; '
            y = calculate_css(target_obj)
            css += '\n\n' + css_dims + '\n' + y + '\n' + '}'
        else:
            css_dims = '#' + svg_ID + '{ width:' + str(rem_width) + 'rem; height:' + str(rem_height) + 'rem; }'
            css += '\n\n' + css_dims

        svg += '\n' + svg_content
 
    return svg, css

#———————————————————————————————————————— calculate_css(this_svg):

def calculate_css(this_svg):
    pos = this_svg.position
    cor = this_svg.corner
    horz = this_svg.horz_offset
    vert = this_svg.vert_offset

    if cor == 'bottom left' or cor == 'bottom right':
        vert = 0 - vert

    if cor == 'top right' or cor == 'bottom right':
        horz = 0 - horz

    posit  = dic_position(pos)
    offset = dic_corners(cor, pos)

    xoff = str(horz/10) + 'rem'
    yoff = str(vert/10) + 'rem'
    offset = offset.replace('xrem', xoff)
    offset = offset.replace('yrem', yoff)
    return posit + offset
  
#———————————————————————————————————————— dic_position(pos):

def dic_position(pos):
    if pos != 'absolute' and pos != 'floating' and pos != 'none': return '/* invalid svg position ' + pos + ' */'
    return {
        'absolute': 'position: absolute;\n',
        'floating': 'position: fixed;\n',
        'none'        : '',
    }[pos]

#———————————————————————————————————————— dic_corners(cor, pos):

def dic_corners(cor, pos):
    if pos != 'absolute' and pos != 'floating' and pos != 'none': return '/* invalid svg position ' + pos + ' */'
    if pos ==  'none': return ''
    return {
        'top left'    : 'left: xrem; right: ; top: yrem; bottom: ;\n',
        'top right'   : 'left: ; right: xrem; top: yrem; bottom: ;\n',
        'bottom right': 'left: ; right: xrem; top: ; bottom: yrem;\n',
        'bottom left' : 'left: xrem; right: ; top: ; bottom: yrem;\n',
    }[cor]


#———————————————————————————————————————— fin

# extra info
#   positions = ('absolute', 'floating', 'none',)
#   corners = ('top left', 'top right', 'bottom left', 'bottom right',)

#   css_id = models.CharField(max_length=200, default='', verbose_name='object ID',)
#   position = models.CharField(max_length=255, default='absolute', choices=Choices(*positions), verbose_name='placement')
#   corner = models.CharField(max_length=255, default='top left', choices=Choices(*corners), verbose_name='reference corner')
#   horz_offset = models.PositiveSmallIntegerField(default=0, verbose_name='horizontal offset (px)',)
#   vert_offset = models.PositiveSmallIntegerField(default=0, verbose_name='vertical offset (px)',)
