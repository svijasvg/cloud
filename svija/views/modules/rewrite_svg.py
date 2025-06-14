
#:::::::::::::::::::::::::::::::::::::::: rewrite_svg.py

# import urllib # REMOVE WHEN FIX IS DONE
# new_font = Font.objects.create( adobe_sheet='debug text', svg_ref = 'debug' ); new_font.save

#———————————————————————————————————————— notes
#
#   the point is that this program does any modifications of
#   the actual svg, and returns SVG + info about it
#
#   changes 230705: this program no longer handles font css
#   it only checks if there are fonts that aren't already in DB
#   get_fonts.py handles the rest
#   removes 1st lines of SVG (XML)
#
#   add a unique ID based on filename if necessary
#
#   change generic CSS classes to unique classes
#
#   update font definitions
#
#———————————————————————————————————————— import

import os, re, io

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils.translation import gettext as _
from svija.models import Font


# settings_id is either svg_filename or an existing ID (layer name or in module settings)

def rewrite_svg(raw_name, svg_path, settings_id, use_p3, is_page, object_name):

#———————————————————————————————————————— initialization

  svg_modifier    = 'svg_'
  img_modifier    = 'img_'
  style_modifier  = 'cls_'
  clip_modifier   = 'clp_'
  linear_modifier = 'lin_'
  radial_modifier = 'rad_'

  width = height = 0
  first_line     = ''
  final_svg      = ''
  debug          = 'working'
  px_width       = 0
  px_height      = 0
  new_format     = True       # x2F or data-name

  defs_section   = False      # are we in def section at top of SVG?
  image_ids      = {}         # image id's that are changed in defs section
                              # and need to be updated in rest of file

#———————————————————————————————————————— svg, img & style ids

  raw_name = make_safe(raw_name)

  if settings_id != '':
    svg_id         = make_safe(settings_id)
  else:
    svg_id         = svg_modifier + raw_name

  img_id           = img_modifier + raw_name
  style_id         = style_modifier + raw_name
  clip_id          = clip_modifier + raw_name
  linear_id        = linear_modifier + raw_name
  radial_id        = radial_modifier + raw_name

  #———————————————————————————————————————— read SVG file

  with open(svg_path, 'r', encoding='utf-8') as f:
    raw_svg = f.read()
    svg_lines = raw_svg.split('\n')

  #———————————————————————————————————————— delete first line if <?xml...

  if '<?xml'      in svg_lines[0]: svg_lines.pop(0)
  if 'Generator:' in svg_lines[0]: svg_lines.pop(0)

  #———————————————————————————————————————— remove meta tab with AI-generated manifest

# <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1200 1500"><metadata><c2pa:manifest xmlns:c2pa="http://c2pa.org/manifest">AAA0RGp1bWIAAAAea+yT6MTKXSbeDEDLtPb5ABMN/TNxKIkmIk+MkI5SPjlr/AvLUhYXkk5e+7k3UPPdaz41gx0T</c2pa:manifest></metadata>

  if 'c2pa' in svg_lines[0]:
    before, sep, after = svg_lines[0].partition('<metadata')
    svg_lines[0] = before


#:::::::::::::::::::::::::::::::::::::::: exit if old-format SVG

  #———————————————————————————————————————— DOCUMENTATION: old or new format SVG?
  #
  # original format (save as):
  #
  # <?xml version="1.0" encoding="utf-8"?>
  # <!-- Generator: Adobe Illustrator 27.0.0, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
  # <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
  #    viewBox="0 0 1200 1200" style="enable-background:new 0 0 1200 1200;" xml:space="preserve">
  # <style type="text/css">
  #   .st0{fill:#FFFFFF;}
  #   .st1{opacity:0;fill:#FF00AD;}
  #
  # old format (export):
  #
  # <?xml version="1.0" encoding="utf-8"?>
  # <!-- Generator: Adobe Illustrator 27.9.0, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
  # <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
  #    viewBox="0 0 1200 1200" style="enable-background:new 0 0 1200 1200;" xml:space="preserve">
  # <style type="text/css">
  #   .st0{fill:#FFFFFF;}
  #   .st1{font-family:'Verdana-Bold';}
  #   .st2{font-size:21px;}
  # </style>
  #
  # new format (export):
  #
  # <?xml version="1.0" encoding="UTF-8"?>
  # <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 300 5110">
  #   <defs>
  #     <style>
  #       .cls-1 {
  #
  #———————————————————————————————————————— test for x2F SVG
  #
  # data-name svg has <style> · x2F SVG has <style type="text/css">

# either 5th line contains old style or 4th line contains new style

  for x in range(1,4):
    if 'style type' in svg_lines[x]:
      new_format = False
  
  #———————————————————————————————————————— exit with error if x2F SVG

  if not new_format:
    err_msg_pre = '<pre class=svgError>'
    err_msg_txt = _('was created with an unsupported Illustrator version')
    err_msg_url = '<a href=https://tech.svija.com/illustrator-version target=_blank>tech.svija.com</a>'

    err_msg_txt = err_msg_txt.replace('link', err_msg_url)
    return 'xxx', 0, 0, err_msg_pre + raw_name + err_msg_txt + '</pre>'


#:::::::::::::::::::::::::::::::::::::::: get font info for newly-used fonts

  #———————————————————————————————————————— initialization

  existing_fonts      = Font.objects.all()
  new_fonts           = []
  css_first, css_last = css_range(svg_lines)

  #———————————————————————————————————————— ▼ loop adding new fonts to new_fonts
 
  for x in range(css_first, css_last):

    if 'font-family' in svg_lines[x]:

      #———————————————————————————————————————— get svg reference and font family

      # .cls-2, .cls-3, .cls-4, .cls-5, .cls-6 {
      #   font-family: OpenSans-Light, 'Open Sans';
#  or #   font-family: Kamerik105W00-Bold, Kamerik105W00-Bold;
      #   font-weight: 300;
      # }

      svg_ref_section, font_family = svg_lines[x].split(', ', 1)

      svg_ref     = svg_ref_section.split('family: ')[1].replace('"', '')
      font_family = font_family[0:-1]

      #———————————————————————————————————————— if font is already listed, skip the rest of the loop

      if font_exists(svg_ref, existing_fonts): continue

      #———————————————————————————————————————— get associated classes

      classes = extract_classes(svg_lines[x-1])   # array of .cls-# classes to which this font applies

      #———————————————————————————————————————— determine weight and style
      #                                         search ten lines ahead

      font_weight = ''   # normal CSS font-weight value
      font_style  = ''   # normal CSS font-style value

      for y in range(x, x+10):
        if '}' in svg_lines[y]: break

        if 'font-weight' in svg_lines[y]:
          font_weight = extract_weight_style('weight', svg_lines[y])
        if 'font-style' in svg_lines[y]:
          font_style = extract_weight_style('style', svg_lines[y])

  #———————————————————————————————————————— ▲ end loop by appending new font

      if font_family[0:1] == "'":
        font_family = font_family[1:-1] # remove quotes

      new_font = {
        'svg_ref': svg_ref,
        'family' : font_family,
        'weight' : font_weight,
        'style'  : font_style,
        'classes': classes,
      }

      new_fonts.append(new_font)

  #———————————————————————————————————————— ▼▲ loop through css to get font weight/style defs

  # some weights and styles are listed separately from the
  # font-family definition, so we loop through the CSS looking
  # for style info, then match with font-family via classes

  for x in range(css_first, css_last):
    xstr = str(x)
    # look for font-weight where previous line is not font-family
    if 'font-weight' in svg_lines[x] and 'font-family' not in svg_lines[x-1] :
      classes = get_class_list(svg_lines, x)
      for font_object in new_fonts:
        if classes_match(classes, font_object['classes']):
          valstr = svg_lines[x][21:-1]
          font_object['weight'] = valstr
          
    # look for font-style where previous line is not font-family
    if 'font-style' in svg_lines[x] and 'font-family' not in svg_lines[x-1] :
      classes = get_class_list(svg_lines, x)
      for font_object in new_fonts:
        if classes_match(classes, font_object['classes']):
          valstr = svg_lines[x][20:-1]
          font_object['style'] = valstr

  #———————————————————————————————————————— ▼▲ add new fonts

  for font_object in new_fonts:
    new_font = Font.objects.create(
      svg_ref = font_object['svg_ref'],
      family  = font_object['family'],
      weight  = font_object['weight'],
      style   = font_object['style'],
      enabled = True,
    )

    new_font.save


#:::::::::::::::::::::::::::::::::::::::: process SVG: unique id's & P3 color
  
  #———————————————————————————————————————— ▼ main loop to process SVG line by line

  line_number = 0
  lines_quantity = len(svg_lines)

  while True:
    if line_number == lines_quantity: break # we're done

    line = svg_lines[line_number]
    line = remove_leading_space(line)

    #———————————————————————————————————————— keep 1st line to replace ID when done

    if line_number == 0:
      first_line = line

    #———————————————————————————————————————— get dimensions from viewbox value in svg tag

    # <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="260.1px"
    # height="172.6px" viewBox="0 0 260.1 172.6" style="enable-background:new 0 0 260.1 172.6;" xml:space="preserve">

    # <svg version="1.1" id="zone_x2F_mainMenu_x2F__x3C_30_x2F__x25_150"
    # xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 500 150"
    # style="enable-background:new 0 0 500 150;" xml:space="preserve">

    if line_number == 0:
      parts1 = line.split('viewBox="')
      parts2 = parts1[1].split('"') # edited 220720 to remove space following double quote for when viewBox is last on the line
      viewBox = parts2[0]
      dimensions = viewBox.split(' ')
      px_width = float(dimensions[2])
      px_height = float(dimensions[3])
#     return 'zzz', 1200, 1200, '<pre style="font-size:30px">'+str(px_width)+':'+str(px_height)+'</pre>'

    #———————————————————————————————————————— replace style definitions at top of SVG √

    # https://docs.python.org/3.3/tutorial/introduction.html#lists

    # new SVG style as of April 2024:
    #
    #      .cls-1, .cls-2, .cls-3, .cls-4, .cls-5, .cls-6, .cls-7, .cls-8, .cls-9, .cls-10, .cls-11, .cls-12, .cls-13, .cls-14, .cls-15 {
    #        stroke-miterlimit: 10;
    #      }

    if line[0:1] == '.':
      line = line.replace('.cls-', '.' + style_id + '-')

    #———————————————————————————————————————— COMMENTED OUT remove font-family extra definitions
    # 
    #   Adobe SVG's have double font family listings, and the second
    #   - is unnecessary
    #   - provokes display problems (8 font family, unquoted)
    #   so we can slightly reduce file size and complexity by
    #   removing the second family list

#   if 'font-family:' in line:
#     line = line.split(', ')[0] + ';'

    #———————————————————————————————————————— replace 'url(#linear-gradient-3);' style definitions at top of SVG √

    if line[0:16] == 'clip-path: url(#':
      line = line.replace('clippath', clip_id)

    if line[0:11] == 'fill: url(#' or line[0:13] == 'stroke: url(#' :
      line = line.replace('linear-gradient', linear_id)
      line = line.replace('radial-gradient', radial_id)

    #———————————————————————————————————————— add P3 color definition
    # fill:#FFFFFF, stroke:#9537FF

    if use_p3:
      hash = ' #'

      if line.find('fill:' + hash) >= 0 or line.find('stroke:' + hash) >= 0 or line.find('stop-color:' + hash) >= 0:
        line = add_p3(line, hash) 

#            .clssvg_Footer-12 {
#                fill: #2c2c2c;
#            }
#
#            .clssvg_Footer-52 {
#                stroke: #2f2d2c;
#                stroke-linecap: round;
#                stroke-linejoin: round;
#                stroke-width: 1.195px;
#            }

    #———————————————————————————————————————— change classes to include SVG name

    if line.find('class="cls-') > 0:
      line = re.sub(r'([\"," "])cls-([0-9]*)(?=[\"," "])', r'\1'+ style_id +'-'+r'\2', line)


#   <svg id="svg_AcclrateurCPcarte" data-name="avant animation" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" viewBox="0 0 1200 563">
#       <defs>
#           <style>
#           .cls_AcclrateurCPcarte-1 {
#               fill: none;
#               stroke: url(#linear-gradient);
#               stroke-miterlimit: 10;
#               stroke-width: 5px;
#           }
#           </style>
#           <linearGradient id="grd_AcclrateurCPcarte" x1="510.5" y1="176.833" x2="510.5" y2="257.833" gradientUnits="userSpaceOnUse">
#               <stop offset="0" stop-color="#c1c4cf"/>
#               <stop offset=".644" stop-color="#004955"/>
#           </linearGradient>
#       </defs>
#       <rect class="cls_AcclrateurCPcarte-1" x="442.833" y="179.333" width="135.333" height="76"/>
#   </svg>

    #———————————————————————————————————————— change ID's to include SVG name

    if line.find('id="clippath') > 0:
      line = re.sub(r'clippath', r''+clip_id, line)
    if line.find('id="linear-gradient') > 0:
      line = re.sub(r'linear-gradient', r''+linear_id, line)
    if line.find('id="radial-gradient') > 0:
      line = re.sub(r'radial-gradient', r''+radial_id, line)

    #———————————————————————————————————————— update image defs to include SVG name
    
    # because otherwise two svg's on the page will have images with id "image-2"

    # at top:
    # defs_section   = False      # are we in def section at top of SVG?
    # image_ids      = {}         # image id's that are changed in defs section

    if line[0:6] == "<defs>":
      defs_section = True
    elif line[0:7] == "</defs>":
      defs_section = False

    if defs_section:
      if line[0:11] == '<image id="':
        parts = line.split('"')
        orig_id = parts[1]
        new_id  = img_id + orig_id[5:len(orig_id)]
        parts[1] = new_id
        line = '"'.join(parts)

# python 3.10 only
#         image_ids |= [(orig_id+'"/>', new_id+'"/>')]
        image_ids[orig_id+'"/>'] = new_id+'"/>'

#  <image id="image" width="1196" height="2200" xlink:href="../../Links/Accueil MB fusée.jpg"/>
#  <image id="image-2" width="10" height="64" xlink:href="../../Links/shadow section.png"/>

    #———————————————————————————————————————— update images uses to include SVG name

    if not defs_section:
      if line[0:5] == '<use ':
        parts = line.split('xlink:href="#')
        if len(parts) > 1:
          current_id = parts[1]
          line = ':'+current_id+':'+line

          if image_ids.get(current_id) is not None:
            parts[1] = image_ids[current_id]
            line = 'xlink:href="#'.join(parts)

    #———————————————————————————————————————— COMMENTED OUT fix mixed text weight problem 
    #                                         search for <tspan x="400.88" where x != 0

#   exp = r'tspan x=\"[1-9]'
#   regex = re.compile(r'tspan x=\"[1-9][0-9,\.]*\" y=\"[0-9,\.]*\"')
#   if (re.search(exp, line)):
#     line = clean_tspans(line)
  
    #———————————————————————————————————————— COMMENTED OUT get id if layer like "id example" exists 
    #                                         note that this means the ID could change at the end,
    #                                         so .st[id]8 won't correspond

#     if line[1:10] == 'g id="id_':
#       parts = line.split('"')
#       svg_id = parts[1][3:]

    #———————————————————————————————————————— ▲ close main loop

    if line_number > 0:
      final_svg += line

    line_number += 1

  #———————————————————————————————————————— add or correct with new ID
  #                                         single-layer AI docs have ID with layer name
  #                                         IF layer name is not just <Layer 1>

  # <svg id="Fond" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" viewBox="0 0 1200 2100">
  if first_line.find('id="') > 0:
    parts = first_line.split('"')
    parts[1] = svg_id
    first_line = '"'.join(parts)
  else:
    replacement = '<svg id="' + svg_id + '"'
    first_line = first_line.replace('<svg', replacement, 1)
  

#:::::::::::::::::::::::::::::::::::::::: process SVG: accessibility
  
  #———————————————————————————————————————— add aria accesibility tags

  if is_page:
    replacement = '<svg aria-label="content" aria-description="' + object_name + '" aria-details="accessSvija"'
  else:
    replacement = '<svg aria-label="menu element" aria-description="' + object_name + '" aria-details="linksSvija"'

  first_line = first_line.replace('<svg', replacement, 1)


  return svg_id, px_width, px_height, first_line+final_svg

#:::::::::::::::::::::::::::::::::::::::: functions

#———————————————————————————————————————— css_range(lines)
#
#   given the lines of an SVG file as an array
#   returns the lines number of the first and last lines
#   of CSS code (excluding the html tags)

def css_range(lines):

  css_first = 0
  css_last  = 0

  for x in range(0, len(lines)-1):

    if '<style>' in lines[x]:
      css_first = x + 1
      
    if '</style>' in lines[x]:
      css_last = x - 1

  return css_first, css_last

#———————————————————————————————————————— classes_match(classes, font_object) TO PROGRAM

#   accepts two arrays containg values like '.cls-23'
#   if they both contain the same element return true

def classes_match(list1, list2):
  for x in range(len(list1)):
    for y in range(len(list2)):
      if list1[x] == list2[y]: return True

  return False

#———————————————————————————————————————— get_class_list(svg_lines, x) ⚠️  INFINITE LOOP RISK

#   x is a line in SVG containing either 'font-style' or 'font-weight'
#   and where the previous line did not contain 'font-family'
#   meaning that it's font information in the CSS separately from the family
#
#   we are looking for a line that resembles this:
#
#     .cls-8, .cls-11 {

def get_class_list(svg_lines, x):
  if '.cls-' in svg_lines[x-1]:
    str = svg_lines[x-1][6:-2] # strip initial spaces & final brace
    return str.split(', ')

  return get_class_list(svg_lines, x-1)

#———————————————————————————————————————— extract_classes(str)

#      .cls-8, .cls-43, .cls79 { 

def extract_classes(str):
  str = str[6:-2]
  return str.split(', ')

#———————————————————————————————————————— extract_weight_style(which, str)

def extract_weight_style(which, str):
  trash, result  = str.split('font-' + which + ': ')
  return result[:-1]

#———————————————————————————————————————— font_exists(line_ref, existing_fonts)

def font_exists(line_ref, existing_fonts):
   occurences = [x for x in existing_fonts if line_ref == x.svg_ref]

   if len(occurences) != 0: return True
   else: return False

#———————————————————————————————————————— NO REFERENCE TO THIS update_css(google_font, style_string)

# line_parts[1] = update_css(google_font, line_parts[1])

def update_css(google_font, style_string):

  famly_given = "'" + google_font[0].family + "';"
  style_given = google_font[0].style.lower()

  # these are not currently used
  weights = ['100','200','300','400','500','600','700','800','900','Thin','ExtraLight','Light','Regular','Medium','SemiBold','Bold','ExtraBold','Heavy','Black',]
  styles = ['Normal','Italic','Oblique',]
  widths = ['Condensed', 'Extended',]

  sty = wgt = ''

  if style_given.find('italic') > -1:
    sty = 'font-style:italic;'
    wgt = style_given.replace('italic','')
  elif style_given.find('oblique') > -1:
    sty = 'font-style:oblique;'
    wgt = style_given.replace('oblique','')
  elif style_given.find('normal') > -1:
    sty = 'font-style:normal;'
    wgt = style_given.replace('normal','')
  else:
    wgt = style_given

  if wgt != '':
    wgt = 'font-weight:' + wgt + ';'

  style_string = famly_given + wgt + sty
  style_string = style_string[0:-1]
  return style_string

#———————————————————————————————————————— make_safe(css_id)

# https://regex101.com

def make_safe(css_id):

  css_id = css_id.replace('.svg','')

# per.iod in na,me.svg
  # ord returns unicode code of character
  # map executes function for each item in iterable
# translation_table = dict.fromkeys(map(ord, ' \'",.!@#$'), '-')
# css_id = css_id.translate(translation_table)
# value = css_id

  value = re.sub("[^A-Za-z0-9-_]", "", css_id)
  return value 

#———————————————————————————————————————— get_xy_content(str)

# input: <tspan x="0" y="0" class="st2 st3">ARTISTS</tspan>

# error caused by
# <text transform="matrix(1 0 0 1 39.5131 71.2745)"><tspan x="0" y="0" class="st0 st1 st2">artboard </tspan><tspan x="96.059" y="0" class="st3 st4 st2">cp</tspan><tspan x="124.066" y="0" class="st0 st1 st2"> · computer 1200px</tspan></text>

def get_xy_content(str):
  values = str.split("\"",4)
  x      = values[1]
  y      = values[3]
  rest   = values[4]

  rest_parts_1 = rest.split(">",1)  # split at first >
  half_two = rest_parts_1[1]        # keep second part
  rest_parts_2 = half_two.split("</tspan")  # split at end of tspan
  content = rest_parts_2[0]

  return x, y, rest, content

#———————————————————————————————————————— add_p3(orig_line)

# adds definition after fill:#FFFFFF, stroke:#9537FF
# called line 75

def add_p3(orig_line, hash):

  new_line = orig_line
  new_line = color_replace(new_line, 'fill:', hash)
  new_line = color_replace(new_line, 'stroke:', hash)
  new_line = color_replace(new_line, 'stop-color:', hash)

  return new_line

#———————————————————————————————————————— color_replace(orig_line, property)
#
#    replace color of a given property

def color_replace(orig_line, property, hash):
  blocks = orig_line.split(property + hash) # 'fill:#' for example

  new_line = blocks[0]
  for x in range(0, len(blocks)-1):

    block_parts = blocks[x+1].split(';', 1)

    hex_color = block_parts[0]

    if len(block_parts) > 1:
      rest = block_parts[1]
    else:
      rest = ''

    p3_color  = hex_to_p3(hex_color)
    new_line += property + hash + hex_color + ';' + property + p3_color + ';' + rest

  return new_line

#———————————————————————————————————————— hex_to_p3(hex_color)
#                                         accepts format #45ED8F

def hex_to_p3(hex_color):
  hex_color = sixify(hex_color)

  r = hex_to_int(hex_color[0:2])
  g = hex_to_int(hex_color[2:4])
  b = hex_to_int(hex_color[4:6])
  return 'color(display-p3 '+ r + ' ' + g + ' ' + b + ')'

#———————————————————————————————————————— sixify(hex_color)

def sixify(hex_color):
  if len(hex_color) > 3:
    return hex_color

  else:
    st1 = hex_color[0:1]+hex_color[0:1]
    st2 = hex_color[1:2]+hex_color[1:2]
    st3 = hex_color[2:3]+hex_color[2:3]
    return st1 + st2 + st3

#———————————————————————————————————————— hex_to_int(raw_hex)
#                                         numbers starting 0x are hexadecimal

def hex_to_int(raw_hex):

  hex = '0x'+raw_hex
  p3 = int(hex, 0)
  p3 = round(p3/255,3)
  return str(p3)

#———————————————————————————————————————— remove_leading_space(text)

def remove_leading_space(text):
  return re.sub(r"^\s+","",text)


#:::::::::::::::::::::::::::::::::::::::: fin

