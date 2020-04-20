#———————————————————————————————————————— svg.py
#
#   remove 1st two lines of SVG (XML)
#
#   add a unique ID based on filename if necessary
#
#   change generic CSS classes to unique classes
#
#   update font definitions
#
#———————————————————————————————————————— program

import os, re, io
from svija.models import Font
from django.core.exceptions import ObjectDoesNotExist

def clean(file_path, file_name):

    # if unspecified, ID will be filename with extension removed (-en.svg)
    svg_ID         = cleanup(file_name)
    width = height = 0
    line_number    = 2
    first_line     = ''
    final_svg      = ''

    #———————————————————————————————————— list of woff & google fonts in DB

    goog_fonts    = Font.objects.filter(google=True)
    file_fonts    = Font.objects.filter(google=False)
    fonts_to_add  = []

    #———————————————————————————————————— read in the SVG file

    with open(file_path, 'r', encoding='utf-8') as f:
        raw_svg = f.read()
        svg_lines = raw_svg.split('\n')

    #———————————————————————————————————— main loop to process SVG line by line

    lines_quantity = len(svg_lines)
    while True:

        if line_number == lines_quantity-1: break # we're done
        line = svg_lines[line_number]

        #———————————————————————————————— keep 1st line to update ID when done

        if line_number == 2:
            first_line = line

        #———————————————————————————————— get dimensions from viewbox value in svg tag

        # <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="260.1px"
        #	 height="172.6px" viewBox="0 0 260.1 172.6" style="enable-background:new 0 0 260.1 172.6;" xml:space="preserve">

        if line_number == 3:
            parts1 = line.split('viewBox="')
            parts2 = parts1[1].split('" ')
            viewBox = parts2[0]
            dimensions = viewBox.split(' ')
            px_width = float(dimensions[2])
            px_height = float(dimensions[3])

        #———————————————————————————————— replace '.st0' style definitions at top of SVG

        if line[1:4] == '.st':
            parts = line.split('.st')
            line = '\t.st' + svg_ID + parts[1]

        #———————————————————————————————— change <path class="st2" to <path class="st[id]2"
        #———————————————————————————————— change <rect id="SVGID_53_" to <rect id="[id]_53_"

        if line.find('class="st') > 0:
            line = re.sub(r'([\"," "])st([0-9]*)(?=[\"," "])', r'\1st'+svg_ID+r'\2', line)

        if line.find('SVGID_') > 0:
            line = re.sub(r'SVGID_', r''+svg_ID+'_', line)

        #———————————————————————————————— fix mixed text weight problem
        #
        # delete coords for <tspan x="400.88" y="147">some text</tspan>

        # regex = tspan x=\"[1-9]
        exp = r'tspan x=\"[1-9]'
        regex = re.compile(r'tspan x=\"[1-9][0-9,\.]*\" y=\"[0-9,\.]*\"')
        if (re.search(exp, line)):
          line = regex.sub('tspan', line)

        #———————————————————————————————— get id if layer like "id example" exists
                                        # note that this means the ID could change at the end,
                                        # so .st[id]8 won't correspond

        if line[1:10] == 'g id="id_':
            parts = line.split('"')
            svg_ID = parts[1][3:]

        #————————————————————————————————— find fonts
                                         # .st2{font-family:'Signika-Regular';}
                                         # google font: need to use google-style CSS
                                         # missing font: need to add to fonts DB
                                 
        if line[1:4] == '.st':
            if line.find('family') > 0:
                line_parts = line.split("'")
                css_ref = line_parts[1]

                # if it is a google font already in DB
                # replace Illustrator-style def with Google's
                goog_font = [x for x in goog_fonts if x.name == css_ref]

                if len(goog_font) > 0:
                    line_parts[1] = update_css(goog_font, line_parts[1])
                    line = ''.join(line_parts)
                else:
                    file_font = [x for x in file_fonts if x.name == css_ref]
                    if len(file_font) <= 0:
                        fonts_to_add.append(css_ref)

        #————————————————————————————— close main loop

        if line_number > 2:
            final_svg += '\n' + line;
        line_number += 1

    #—————————————————————————————————————— add any missing fonts to DB

    fonts_to_add = remove_duplicates(fonts_to_add)

    for css_ref in fonts_to_add:
        new_font = create_new_font(css_ref, Font())
        p = Font.objects.create(name = new_font.name, family = new_font.family, style=new_font.style, source=new_font.source, google=False, active=False)
        p.save

    #—————————————————————————————————————— add new ID if necessary
                                          # single-layer AI docs have ID with layer name

    if first_line.find('id="') > 0:
        parts = line.split('"')
        svg_ID = parts[3]
    else:
        first_line = first_line.replace('<svg ', '<svg id="' + svg_ID + '" ', 1)

    #—————————————————————————————————————— return SVG ID, dimensions & contents

    return svg_ID, px_width, px_height, first_line+final_svg

#———————————————————————————————————————————————————————————————————————————————————————————
#———————————————————————————————————————— functions ————————————————————————————————————————
#———————————————————————————————————————————————————————————————————————————————————————————

def create_new_font(css_ref, new_font):

    name = family = css_ref
    weight = style = width = ''
    source = 'SOURCE NEEDED'

    weights = ['100','200','300','400','500','600','700','800','900','Thin','ExtraLight','Light','Regular','Medium','SemiBold','Bold','ExtraBold','Heavy','Black',]
    styles = ['Normal','Italic','Oblique',]
    widths = ['Condensed', 'Extended',]

    for this_one in weights:
        if css_ref.lower().find(this_one.lower()) > -1:
            weight = this_one
            regx = re.compile(r'[-]?'+this_one, re.IGNORECASE)
            family = regx.sub('', family)
            break

    for this_one in styles:
        if css_ref.lower().find(this_one.lower()) > -1:
            style = this_one
            regx = re.compile(r'[-]?'+this_one, re.IGNORECASE)
            family = regx.sub('', family)
            break

    for this_one in widths:
        if css_ref.lower().find(this_one.lower()) > -1:
            width = this_one
            regx = re.compile(r'[-]?'+this_one, re.IGNORECASE)
            family = regx.sub('', family)
            break

    # change OpenSans to Open Sans
    regx = re.compile(r'([a-z])([A-Z])')
    family = regx.sub(r'\1 \2', family)

    weight_style = weight + style + width
    if weight_style == '':
        weight_style = 'Regular'

    new_font.name, new_font.family, new_font.style, new_font.source = name, family, weight_style, source

    return new_font

# http://dev.svija.com/en/print
# not finding "'Signika-Regular';"
# 	.stLayer_12{font-family:'Signika-Regular';}

#———————————————————————————————————————— google font function
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

#———————————————————————————————————————— remove special characters

def cleanup(filename):
# per.iod in na,me.svg
  translation_table = dict.fromkeys(map(ord, ' \'",.!@#$'), '-')
  filename = filename.translate(translation_table)
  return filename[:-4]

#———————————————————————————————————————— remove duplicates

def remove_duplicates(font_array):
    results = list( dict.fromkeys(font_array) )
    return results

#———————————————————————————————————————— fin
