#———————————————————————————————————————— svg.py
#
#        remove XML (1st two lines)
#
#        remove pixel dimensions if present
#        equivalent of checking "responsive" in Illustrator
#
#        add a unique ID based on filename if necessary
#
#        change generic st classes to unique classes
#        based on filename
#
#———————————————————————————————————————— program

import os, re, io
from svija.models import Font
from django.core.exceptions import ObjectDoesNotExist

def clean(svg_path, svg_name):

    # if unspecified, ID will be filename with extension removed (-en.svg)
    svg_ID         = svg_name[:-4]
    add_ID         = True
    width = height = 0
    line_number    = -1
    final_svg      = ''
    new_fonts, fonts_file, fonts_goog = [], [], []

    #———————————————————————————————————— list of woff & google fonts in DB
    # could be rewritten in three lines

    fonts_db = Font.objects.all()
    for this_font in fonts_db:
        if this_font.google:
            fonts_goog.append(this_font)
        else:
            fonts_file.append(this_font)

    with open(svg_path, 'r', encoding='utf-8') as f:
        raw_svg = f.read()
        svg_lines = raw_svg.split('\n')

    #———————————————————————————————————— main loop to process SVG line by line

    while True:

        line_number = line_number + 1
        if line_number == len(svg_lines): break # we're done

        line = svg_lines[line_number - 1]
        if line[0:5] == '<?xml': continue
        if line[0:4] == '<!--': continue

        #———————————————————————————————— if svg has an ID, use it

        # single-layer AI docs have svg ID named for layer
        # <svg version="1.1" id="Layer_1" xmlns="http:
        if line[0:4] == '<svg':
            if line.find('id="') > 0:
                parts = line.split('"')
                svg_ID = parts[3]
                add_ID = False

        #———————————————————————————————— get dimensions from viewbox value in svg tag

        # <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="260.1px"
        #	 height="172.6px" viewBox="0 0 260.1 172.6" style="enable-background:new 0 0 260.1 172.6;" xml:space="preserve">

        if line_number < 5 and line.find('viewBox') > 0:
            parts1 = line.split('viewBox="')
            parts2 = parts1[1].split('" ')
            viewBox = parts2[0]
            dimensions = viewBox.split(' ')
            px_width = float(dimensions[2])
            px_height = float(dimensions[3])

        #————————————————————————————————— find fonts
        # .stLayer_12{font-family:'Signika-Regular';}
        #————————————————————————————————————————————

        if line[1:4] == '.st' and line.find('font-family') > 0:
            line_parts = line.split("'")
            css_ref = line_parts[1]

            # if it is a google font already in DB
            # replace Illustrator-style def with Google's
            google_font = [x for x in fonts_goog if x.name == css_ref]
            woff_font = [x for x in fonts_file if x.name == css_ref]

            if len(google_font) > 0:
                line_parts[1] = redefine_styles(google_font, line_parts[1])
                line = ''.join(line_parts)

            # if it's not a woff font already in DB the add it
            elif len(woff_font) <= 0:
                # should be a better way to do this
                font_to_replace = Font()
                new_font = create_new_font(css_ref, font_to_replace)
                new_fonts.append(new_font)

        #———————————————————————————————— replace style definitions at top of SVG
        #———————————————————————————————— and style applications in body of SVG

        if line[1:4] == '.st':
            parts = line.split('.st')
            line = '\t.st' + svg_ID + parts[1]

        if line.find('class="st') > 0:
            line = re.sub(r'([\"," "])st([0-9]*)(?=[\"," "])', r'\1st'+svg_ID+r'\2', line)

        #———————————————————————————————— get id if specified
        #———————————————————————————————— AI file with layer name "id example"

        if line[1:10] == 'g id="id_': svg_ID = line[10:-2]

     #———————————————————————————————— add line into final SVG

        final_svg += '\n' + line;

  #———————————————————————————————————————— add new ID if necessary

    if add_ID:
        final_svg = final_svg.replace('<svg ', '<svg id="' + svg_ID + '" ', 1)

  #———————————————————————————————————————— check font table
  # https://stackoverflow.com/questions/14676613/how-to-import-google-web-font-in-css-file

    # add fonts that were not already in DB to DB
    for each_font in new_fonts:
        try:
            font_obj = Font.objects.get(name = each_font.name)
            rien = 0
        except ObjectDoesNotExist:
            p = Font.objects.create(name = each_font.name, family = each_font.family, style=each_font.style, source=each_font.source, google=False, active=False)
            p.save

    return svg_ID, px_width, px_height, final_svg

#———————————————————————————————————————— functions

def create_new_font(css_ref, new_font):

    name = family = css_ref
    weight = style = width = ''
    source = 'PLEASE ACTIVATE'

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
# line_parts[1] = redefine_styles(google_font, line_parts[1])

def redefine_styles(google_font, style_string):

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

#———————————————————————————————————————— fin
