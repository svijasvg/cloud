
#:::::::::::::::::::::::::::::::::::::::: rewrite_svg.py

#import urllib # REMOVE WHEN FIX IS DONE

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
from svija.models import Font


# settings_id is either svg_filename or an existing ID (layer name or in module settings)

def rewrite_svg(raw_name, svg_path, settings_id, use_p3, is_page, page_title):

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
  new_format     = True       # is it saved "export" instead of "save as" in Svija Tools
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

  #———————————————————————————————————————— list of fonts in DB

  all_fonts   = Font.objects.all()
  fonts_to_add  = []

  #———————————————————————————————————————— read SVG file

  with open(svg_path, 'r', encoding='utf-8') as f:
    raw_svg = f.read()
    svg_lines = raw_svg.split('\n')

  #———————————————————————————————————————— old or new format SVG? EXPLANATION
  #
  # Data-Name format:
  # <?xml version="1.0" encoding="UTF-8"?>
  # <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 300 5110">
  #   <defs>
  #     <style>
  #       .cls-1 {
  # 
  #
  # x2F format
  # <?xml version="1.0" encoding="UTF-8"?>
  # <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 300 5110">
  #   <defs>
  #     <style>
  #       .cls-1 {
  #
  # Save-As format
  # <?xml version="1.0" encoding="utf-8"?>
  # <!-- Generator: Adobe Illustrator 26.0.1, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
  # <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
  # 	 viewBox="0 0 1680 3040" style="enable-background:new 0 0 1680 3040;" xml:space="preserve">
  # <style type="text/css">
  # 	.st0{fill:url(#SVGID_1_);}
  #
  #———————————————————————————————————————— delete first line if <?xml...

  letters = svg_lines[0][2:5]
  if letters == 'xml': svg_lines.pop(0)

  #———————————————————————————————————————— delete first line if <!-- Generator: ...

  letters = svg_lines[0][5:14]
  if letters == 'Generator':
    svg_lines.pop(0)
    new_format = False
  

#:::::::::::::::::::::::::::::::::::::::: old-format SVG

  if not new_format:

    #———————————————————————————————————————— ▼ main loop to process SVG line by line
  
    line_number = 0
    lines_quantity = len(svg_lines)
  
    while True:
      if line_number == lines_quantity: break # we're done
  
      line = svg_lines[line_number]
      line = no_leading_space(line)
  
      #———————————————————————————————————————— keep 1st line to replace ID when done
  
      if line_number == 0:
        first_line = line
  
      #———————————————————————————————————————— get dimensions from viewbox value in svg tag √
  
      # <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="260.1px"
      # height="172.6px" viewBox="0 0 260.1 172.6" style="enable-background:new 0 0 260.1 172.6;" xml:space="preserve">
  
      # <svg version="1.1" id="zone_x2F_mainMenu_x2F__x3C_30_x2F__x25_150"
  	  # xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 500 150"
  	  # style="enable-background:new 0 0 500 150;" xml:space="preserve">
  
      if line_number == 1:
        parts1 = line.split('viewBox="')
        parts2 = parts1[1].split('"') # edited 220720 to remove space following double quote for when viewBox is last on the line
        viewBox = parts2[0]
        dimensions = viewBox.split(' ')
        px_width = float(dimensions[2])
        px_height = float(dimensions[3])
#       return 'zzz', 1200, 1200, '<pre style="font-size:30px">'+line+'</pre>'
#       viewBox="0 0 1200 2437" style="enable-background:new 0 0 1200 2437;" xml:space="preserve">

#       return 'zzz', 1200, 1200, '<pre style="font-size:30px">'+str(px_width)+':'+str(px_height)+'</pre>'
#       <pre style="font-size:30px">1200.0:2437.0</pre>
  
      #———————————————————————————————————————— replace style definitions at top of SVG √
  
      # https://docs.python.org/3.3/tutorial/introduction.html#lists
  
      # new SVG style as of April 2024:
      #
      #      .cls-1, .cls-2, .cls-3, .cls-4, .cls-5, .cls-6, .cls-7, .cls-8, .cls-9, .cls-10, .cls-11, .cls-12, .cls-13, .cls-14, .cls-15 {
      #        stroke-miterlimit: 10;
      #      }
  
      if line[0:3] == '.st':
        parts = line.split('.st')
        line = '.st' + svg_id + parts[1]
  
      #———————————————————————————————————————— add P3 color definition
      # fill:#FFFFFF, stroke:#9537FF
  
  #	.st0{fill:#414042;}
  #	.st1{opacity:0.3;fill:#FF00FF;}
  #	.st2{fill:#FFFFFF;}
  #	.st3{font-family:'OpenSans-Semibold';}
  
      if use_p3:
        hash = '#'
  
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
  
      if line.find('class="st') > 0:
        line = re.sub(r'([\"," "])st([0-9]*)(?=[\"," "])', r'\1st'+svg_id+r'\2', line)
  
  
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
  
      if line.find('SVGID_') > 0:
        line = re.sub(r'SVGID_', r'SVGID_'+svg_id+'_', line)
  
      #———————————————————————————————————————— update images uses to include SVG name
  
      if new_format and not defs_section:
        if line[0:5] == '<use ':
          parts = line.split('xlink:href="#')
          if len(parts) > 1:
            current_id = parts[1]
            line = ':'+current_id+':'+line
  
            if image_ids.get(current_id) is not None:
              parts[1] = image_ids[current_id]
              line = 'xlink:href="#'.join(parts)
  
      #———————————————————————————————————————— fix mixed text weight problem COMMENTED OUT
      #                                         search for <tspan x="400.88" where x != 0
  
  #   exp = r'tspan x=\"[1-9]'
  #   regex = re.compile(r'tspan x=\"[1-9][0-9,\.]*\" y=\"[0-9,\.]*\"')
  #   if (re.search(exp, line)):
  #     line = clean_tspans(line)
    
      #———————————————————————————————————————— get id if layer like "id example" exists COMMENTED OUT
      #                                         note that this means the ID could change at the end,
      #                                         so .st[id]8 won't correspond
  
  #     if line[1:10] == 'g id="id_':
  #       parts = line.split('"')
  #       svg_id = parts[1][3:]
  
      #———————————————————————————————————————— find fonts
  
      #    .st2{font-family:'Signika-Regular';}
      #    google font: need to use google-style CSS
      #    missing font: need to add to fonts DB
  
      if line[0:3] == '.st':
        if line.find('family') > 0:

    # if a font-family definition —————————————————————————————————————————————

    # if font doesn't exist, add it to list of fonts-to-add
    # if it does exist:
    #   if it has a family name
    #     if it's not a woff, we add font weight etc. to the svg line
    #     if it is a woff, we do nothing

          line_parts  = line.split("'")
          line_ref    = line_parts[1]
          font_exists = [x for x in all_fonts if x.svg_ref == line_ref]
  
          # font does not exist
          if len(font_exists) == 0:
            fonts_to_add.append(line_ref)
  
          # font exists
          else:
            fonts = Font.objects.filter(Q(enabled=True) & Q(svg_ref = line_ref)).exclude(family = '')

            # only treat fonts with filled-out info
            if len(fonts) != 0:
              font = fonts[0] # result was an array — there's only one

              # woff has absolute priority
              if font.woff == '':
                new_font_info = "'" + font.family + "'; font-weight:" + font.weight + "; font-style: " + font.style
                line = line_parts[0] + new_font_info + line_parts[2]
  
      #———————————————————————————————————————— debugging COMMENTED OUT
  #   fb = urllib.parse.quote(line)
  #   return "lkjsdf", 1200,1200, "<pre style='color:white;font-size:30px;'>" + fb + "</pre>"
  
      #———————————————————————————————————————— ▲ close main loop
  
      if line_number > 0:
        final_svg += '\n' + line
  
      line_number += 1
  
    #———————————————————————————————————————— add missing fonts to DB
  
  # return 'zzz', 1200, 1200, '<pre style="font-size:30px">:'+str(line_number)+':'+line[0:11]+':</pre>'
    fonts_to_add = remove_duplicates(fonts_to_add)
  
    for css_ref in fonts_to_add:
      new_font = Font.objects.create(svg_ref = css_ref, enabled=True)
      new_font.save
  
    #———————————————————————————————————————— add or correct with new ID
    #                                         single-layer AI docs have ID with layer name
    #                                         IF layer name is not just <Layer 1>
  
    # <svg version="1.1" id="Fond" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
    if first_line.find('id="') > 0:
      parts = first_line.split('"')
      parts[3] = svg_id
      first_line = '"'.join(parts)
    else:
      replacement = '<svg id="' + svg_id + '"'
      first_line = first_line.replace('<svg', replacement, 1)
  
  
    return svg_id, px_width, px_height, first_line+final_svg
  
#:::::::::::::::::::::::::::::::::::::::: new-format SVG

  if new_format:

    #———————————————————————————————————————— ▼ main loop to process SVG line by line
  
    line_number = 0
    lines_quantity = len(svg_lines)
  
    while True:
      if line_number == lines_quantity: break # we're done
  
      line = svg_lines[line_number]
      line = no_leading_space(line)
  
      #———————————————————————————————————————— keep 1st line to replace ID when done
  
      if line_number == 0:
        first_line = line
  
      #———————————————————————————————————————— get dimensions from viewbox value in svg tag √
  
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
  
      #———————————————————————————————————————— fix mixed text weight problem COMMENTED OUT
      #                                         search for <tspan x="400.88" where x != 0
  
  #   exp = r'tspan x=\"[1-9]'
  #   regex = re.compile(r'tspan x=\"[1-9][0-9,\.]*\" y=\"[0-9,\.]*\"')
  #   if (re.search(exp, line)):
  #     line = clean_tspans(line)
    
      #———————————————————————————————————————— get id if layer like "id example" exists COMMENTED OUT
      #                                         note that this means the ID could change at the end,
      #                                         so .st[id]8 won't correspond
  
  #     if line[1:10] == 'g id="id_':
  #       parts = line.split('"')
  #       svg_id = parts[1][3:]
  
      #———————————————————————————————————————— find fonts
  
      #    .st2{font-family:'Signika-Regular';}
      #    google font: need to use google-style CSS
      #    missing font: need to add to fonts DB
  
      if line[0:12] == 'font-family:':

    # if a font-family definition —————————————————————————————————————————————

        line_parts_1 = line.split(': ', 1)
        line_parts_2 = line_parts_1[1].split(',', 1)
        line_ref     = line_parts_2[0]
        line_rest    = line_parts_2[1]
        font_exists  = [x for x in all_fonts if x.svg_ref == line_ref]

        # font does not exist
        if len(font_exists) == 0:
          fonts_to_add.append(line_ref)

#       # font exists
#       else:
#         font = Font.objects.filter(Q(enabled=True) & Q(svg_ref = line_ref)).first()

#         # need to delete style info if it's a woff
#         if font.woff != '':
#           repeat = True
#           l = line_number
#           while repeat:
#             l += 1
#             if svg_lines[l].find('font-style') > 0:
#               svg_lines[l] = '/* style deleted */'
#             if svg_lines[l].find('font-weight') > 0:
#               svg_lines[l] = '/* weight deleted */'
#             if svg_lines[l].find('}') > 0:
#               repeat = False
  
      #———————————————————————————————————————— debugging COMMENTED OUT
  #   fb = urllib.parse.quote(line)
  #   return "lkjsdf", 1200,1200, "<pre style='color:white;font-size:30px;'>" + fb + "</pre>"
  
      #———————————————————————————————————————— ▲ close main loop
  
      if line_number > 0:
        final_svg += line
  
      line_number += 1
  
    #———————————————————————————————————————— add missing fonts to DB
  
  # return 'zzz', 1200, 1200, '<pre style="font-size:30px">:'+str(line_number)+':'+line[0:11]+':</pre>'
    fonts_to_add = remove_duplicates(fonts_to_add)
  
    for css_ref in fonts_to_add:
      new_font = Font.objects.create(svg_ref = css_ref, enabled=True)
      new_font.save
  
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
  
    #———————————————————————————————————————— add aria accesibility tags

    if is_page:
      replacement = '<svg aria-label="content" aria-description="' + page_title + '" aria-details="accessSvija"'
    else:
      replacement = '<svg aria-label="menu element" aria-description="' + raw_name + '" aria-details="linksSvija"'

    first_line = first_line.replace('<svg', replacement, 1)
  

    return svg_id, px_width, px_height, first_line+final_svg

#:::::::::::::::::::::::::::::::::::::::: methods

#———————————————————————————————————————— update_css(google_font, style_string)

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

#———————————————————————————————————————— remove_duplicates(font_array)

def remove_duplicates(font_array):
  results = list( dict.fromkeys(font_array) )
  return results

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

#———————————————————————————————————————— def clean_tspans(line) COMMENTED OUT AT CALL
# remove x & y coords from tspan

# fixes problem where Safari cause text tspans to bump into each other
# delete coords for <tspan x="400.88" y="147">some text</tspan>

def clean_tspans(line):

  tspans = line.split('<tspan ')
  first_bit = tspans.pop(0)

  tspans = ['<tspan {0}'.format(i) for i in tspans] # add tspans back to list

  number_of_tspans = len(tspans)
  output = ''

  # go through tspans from last to 2nd (start, end, step)
  # https://stackoverflow.com/questions/4504662/why-does-rangestart-end-not-include-end
  # reverse range ends earlier than expected

  for x in range (number_of_tspans-1, -1, -1):

    this_x, this_y, this_rest, this_content = get_xy_content(tspans[x])

    if this_content == "\t": continue # AI gives tabs an empty tspan

    if x > 0 and this_x != 0:
      prev_x, prev_y, prev_rest, prev_content  = get_xy_content(tspans[x-1])

      # if the Y height is same as previous block, and there's no text separation
      # we get rid of the x & y coordinates
      if this_y == prev_y and prev_content != "\t":
        tspans[x] = '<tspan ' + this_rest # strip coordinates from tspans[x]

    # add a CR for debugging only — it causes Firefbx & Chrome to add whitespace
    output = tspans[x] + "" + output

  output = first_bit + "\n" + output
  return output

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

#———————————————————————————————————————— no_leading_space(text)

def no_leading_space(text):
  return re.sub(r"^\s+","",text)


#:::::::::::::::::::::::::::::::::::::::: fin

