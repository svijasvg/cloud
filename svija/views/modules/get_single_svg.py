
#:::::::::::::::::::::::::::::::::::::::: get_single_svg.py

#———————————————————————————————————————— notes
#
#   used by construct_page.py
#
#   accepts Illustrator file, page width, and use P3
#
#   returns an SVG file, css with dimensions
#   and if it's the basic page, a div with the 
#   appropriate width for pre-setting the HTML page
#
#———————————————————————————————————————— import

import os
import pathlib
import unicodedata
from modules.clean_svg import *


def get_single_svg(parent_obj, screen_code, page_width, use_p3):

#———————————————————————————————————————— if no SVG file

  # if empty module without AI file
  if not hasattr(parent_obj, 'filename'): return '', '', ''

  # if file doesn't exist                  # if it had a filename
  ai_name = parent_obj.filename            # which was subsequently
  if ai_name == '':                        # deleted
    return '', '', ''

  #———————————————————————————————————————— clean AI file path

  # remove everything in beginning of path if necessary
  # /Users/Main/Library/Mobile Documents/com~apple~CloudDocs/sync/svija.dev/sync/test.ai

  ai_name = parent_obj.filename

  if ai_name.find('/') > -1:
    ai_name = ai_name.rpartition("/")[2]
    parent_obj.filename = ai_name
    parent_obj.save()

#———————————————————————————————————————— create SVG path

  raw_name = ai_name[:-3]

  # escape single quotes
# raw_name = raw_name.replace("'", "\\/'")

  svg_name = raw_name + '_' + screen_code + '.svg'

  svija_path = '/sync/SVIJA/SVG Files/'
  abs_path = os.path.abspath(os.path.dirname(__name__))

  svg_path = abs_path + svija_path + svg_name

  # compensate for old version of rsync
  # should have no effect if already normalized
  svg_path = unicodedata.normalize('NFD', svg_path)

  path = pathlib.Path(svg_path)

  #———————————————————————————————————————— if path doesn't work

  if not path.exists():
    #vg = '<!-- missing svg: {} -->'.format(parent_obj.filename)
    #vg = '<!-- missing svg: {} -->\n'.format(svija_path+svg_name)

    alert_msg = '<script>alert("⚠️ get single svg line 108\n\nIllustrator File Missing\\n\\"{}.ai\\" containing artboard \\"{}\\"\\n\\nIf Svija Sync is running:\\n• check Illustrator file name\\n• check artboard name")</script>'

    #lert = alert_msg.format(raw_name, screen_code)
    alert = alert_msg.format(svg_path, screen_code)

    return alert, '', ''

  #———————————————————————————————————————— create temp ID

  prelim_id = 'svg_' + raw_name

  if hasattr(parent_obj, 'css_id'):
    # could be '' if it previously had an id that was later set to ''
    if parent_obj.css_id != '': 
      prelim_id = parent_obj.css_id

  #———————————————————————————————————————— finalize ID, coordinates and content

  svg_id, svg_width, svg_height, svg = clean_svg(svg_path, prelim_id, use_p3)

  if svg_width > page_width:
    page_ratio = svg_height/svg_width
    svg_width = page_width
    svg_height = round(page_width * page_ratio)

  rem_width  = round(svg_width,  3)
  rem_height = round(svg_height, 3)

  #———————————————————————————————————————— create CSS & div if needed

  is_page = str(type(parent_obj)) == "<class 'svija.models.Illustrator'>" 

  if is_page:
    div = '#set_scroll_div{ width:' + str(rem_width) + 'rem; height:' + str(rem_height) + 'rem; }'
    css_dims = '#' + svg_id + '{ width:' + str(rem_width) + 'rem; height:' + str(rem_height) + 'rem; }'
    css = '\n\n' + css_dims
  else:
    div = ''
    css_dims = '#' + svg_id + '{\n'
    css_dims += 'width:' + str(rem_width) + 'rem; height:' + str(rem_height) + 'rem; '

    # take module position into account
    position = calculate_css(parent_obj)
    css = '\n\n' + css_dims + '\n' + position + '\n' + '}'


  return '\n' + svg, css, div

#:::::::::::::::::::::::::::::::::::::::: methods

#———————————————————————————————————————— calculate_css(this_svg):

def calculate_css(this_svg):
  pos = this_svg.position
  cor = this_svg.corner
  horz = this_svg.offsetx
  vert = this_svg.offsety

  if cor == 'bottom left' or cor == 'bottom right':
    vert = 0 - vert

  if cor == 'top right' or cor == 'bottom right':
    horz = 0 - horz

  posit  = dic_position(pos)
  offset = dic_corners(cor, pos)

  xoff = str(horz) + 'rem'
  yoff = str(vert) + 'rem'
  offset = offset.replace('xrem', xoff)
  offset = offset.replace('yrem', yoff)
  return posit + offset
  
#———————————————————————————————————————— dic_position(pos):

def dic_position(pos):
  if pos != 'attached' and pos != 'floating' and pos != 'none': return '/* invalid svg position ' + pos + ' */'
  return {
    'attached': 'position: absolute;\n',
    'floating': 'position: fixed;\n',
    'none'    : '',
  }[pos]

#———————————————————————————————————————— dic_corners(cor, pos):

def dic_corners(cor, pos):
  if pos != 'attached' and pos != 'floating' and pos != 'none': return '/* invalid svg position ' + pos + ' */'
  if pos ==  'none': return ''
  return {
    'top left'  : 'left: xrem; right: ; top: yrem; bottom: ;\n',
    'top right'   : 'left: ; right: xrem; top: yrem; bottom: ;\n',
    'bottom right': 'left: ; right: xrem; top: ; bottom: yrem;\n',
    'bottom left' : 'left: xrem; right: ; top: ; bottom: yrem;\n',
  }[cor]

#———————————————————————————————————————— dic_corners(cor, pos):

def purify(inp):
  oup = inp.replace('&', 'et')
  oup = oup.replace('(', 'lp')
  oup = oup.replace(')', 'rp')
  return oup

#———————————————————————————————————————— extra info
#   positions = ('attached', 'floating', 'none',)
#   corners = ('top left', 'top right', 'bottom left', 'bottom right',)

#   css_id = models.CharField(max_length=200, default='', verbose_name='object ID',)
#   position = models.CharField(max_length=255, default='attached', choices=Choices(*positions), verbose_name='placement')
#   corner = models.CharField(max_length=255, default='top left', choices=Choices(*corners), verbose_name='reference corner')
#   offsetx = models.PositiveSmallIntegerField(default=0, verbose_name='horizontal offset (px)',)
#   offsety = models.PositiveSmallIntegerField(default=0, verbose_name='vertical offset (px)',)


#:::::::::::::::::::::::::::::::::::::::: fin

