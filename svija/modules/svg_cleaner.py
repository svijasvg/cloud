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

# given path to source file & name (need to figure out what to pass exactly)

def clean(svg_source, svg_name):

    # if unspecified, ID will be filename with languager & extension removed (-en.svg)
    svg_ID = svg_name[:-7]

    #svg_source = os.path.abspath(os.path.dirname(__name__)) + '/' + svg_source + '/' + svg_name

    #————————————————————————————————————- initialize values

    width = 0
    height = 0
    line_number = -1
    result = ''
    fonts_found = []
    fonts_woff = []
    fonts_goog = []

    #————————————————————————————————————- list of woff & google fonts

    fonts = Font.objects.all()
    for this_font in fonts:
        if this_font.google:
            fonts_goog.append(this_font)
        else:
            fonts_woff.append(this_font)

    #————————————————————————————————————- read contents of SVG, split into lines

    with open(svg_source, 'r', encoding='utf-8') as f:
        raw_svg = f.read()
        svg_lines = raw_svg.split('\n')

    #————————————————————————————————————- process the SVG line by line

    while True:

        line_number = line_number + 1
        if line_number == len(svg_lines): break # we're done
        line = svg_lines[line_number - 1]

        #————————————————————————————————-- if the AI xml header is there delete it

        if line[0:5] == '<?xml': continue
        if line[0:4] == '<!--': continue

        #———————————————————————————————— if already ID don't need new ID

        if line[0:4] == '<svg':
            if line.find('id="') > 0:
                svg_ID = ''

        #———————————————————————————————— remove pixel dimensions if any

        if line[2:9] == 'viewBox':

            #————————————————————————————-- remove pixel dimensions if any

            if line.find('px" ') > 0:
                parts = line.split('px" ')
                line = '\t ' + parts[-1]

            #————————————————————————————-- extract dimensions from viewBox

            parts = line.split('"')
            viewBox = parts[1]
            dimensions = viewBox.split(' ')
            px_width = float(dimensions[2])
            px_height = float(dimensions[3])

        #————————————————————————————————-- replace style definitions
        #————————————————————————————————-- .st10 creates conflict when multiple svg's on a page
        #————————————————————————————————-- replaced with .st[SVG ID]10

        if line[1:4] == '.st':
            parts = line.split('.st')
            line = '\t.st' + svg_ID + parts[1]

            #————————————————————————————-- find fonts
            #————-- .st24{font-family:'Roboto-Light';}
            #————————————————————————————————————————-

            if line.find('font-family') > 0:
                line_parts = line.split("'")
                found_font = line_parts[1]

                # if it is a google font already in DB
                # replace Illustrator-style def with Google's
                google_font = [x for x in fonts_goog if x.name == found_font]
                if len(google_font) > 0:
                    famly_given = "'" + google_font[0].family + "';"
                    style_given = google_font[0].style.lower()
                    sty = ''
                    wgt = ''

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

                    line_parts[1] = famly_given + wgt + sty
                    line_parts[1] = line_parts[1][0:-1]
                    line = "".join(line_parts)

                # if it's a woff font already in DB
                # then the styles are already correct (SHOULD BE)
                woff_font = [x for x in fonts_woff if x.name == found_font]
                if len(woff_font) > 0:
                    do_nothing = True

                # font is not in DB
                if len(woff_font) <= 0 and len(google_font) <= 0:
                    font_to_replace = fonts[0]
                    fonts_found.append(complicated_function(found_font, font_to_replace))

#                   font_to_replace = fonts[0]
#                   new_weight = ''
#                   new_style = ''

#                   # weights
#                   if found_font.lower().find('bold') > -1:
#                       new_weight = 'Bold'
#                   elif found_font.lower().find('semibold') > -1:
#                       new_weight = 'SemiBold'
#                   elif found_font.lower().find('light') > -1:
#                       new_weight = 'Light'
#                   elif found_font.lower().find('regular') > -1:
#                       new_weight = 'Regular'

#                   # styles
#                   elif found_font.lower().find('italic') > -1:
#                       new_style = 'Italic'
#                   elif found_font.lower().find('oblique') > -1:
#                       new_style = 'Oblique'
#                   elif found_font.lower().find('normal') > -1:
#                       new_style = 'Normal'
#                   else:
#                       something = False
#                   font_to_replace.name = found_font
#                   font_to_replace.family = found_font
#                   font_to_replace.style = new_weight+new_style
#                   font_to_replace.source = 'missing'
#                   fonts_found.append(font_to_replace)

        #————————————————————————————————-- replace style applications
        # class= st2 › staccueil_fr2

        if line.find('class="st') > 0:
            line = re.sub(r'([\"," "])st([0-9]*)(?=[\"," "])', r'\1st'+svg_ID+r'\2', line)

        #————————————————————————————————-- get id if specified

        if line[1:10] == 'g id="id_': svg_ID = line[10:-2]

     #————————————————————————————————-- print this line

        result += '\n' + line;

  #————————————————————————————————————————- add new ID if necessary

    if svg_ID != '':
        result = result.replace('<svg ', '<svg id="' + svg_ID + '" ', 1)

  #————————————————————————————————————————- check font table
  # https://stackoverflow.com/questions/14676613/how-to-import-google-web-font-in-css-file

    # add fonts that were not already in DB to DB
    for each_font in fonts_found:
        try:
            font_obj = Font.objects.get(name = each_font.name)
            rien = 0
        except ObjectDoesNotExist:
            p = Font.objects.create(name = each_font.name, family = each_font.family, style=each_font.style, source=each_font.source, google=False, active=False)
            p.save

    return svg_ID, px_width, px_height, result

#———————————————————————————————————————— functions
# if len(woff_font) <= 0 and len(google_font) <= 0:
#     fonts_found.append(comlicated_function(found_font))

def complicated_function(found_font, font_to_replace):

    font_to_replace.name = found_font
    font_to_replace.family = found_font
    font_to_replace.source = 'PLEASE ACTIVATE'

    weights = ['100','200','300','400','500','600','700','800','900','Thin','ExtraLight' 'Light','Regular','Medium','SemiBold','Bold','ExtraBold','Heavy','Black',]
    styles = ['Normal','Italic','Oblique',]
    widths = ['Condensed', 'Extended',]

    new_weight = ''
    new_style = ''

    for this_one in weights:
        if found_font.lower().find(this_one.lower()) > -1:
            new_weight = this_one

#           found_font = re.sub(
#               r"(?i)^.*interfaceOpDataFile.*$",
#               "interfaceOpDataFile %s" % fileIn,
#               found_font
#           )

    # weights
    if found_font.lower().find('bold') > -1:
        new_weight = 'Bold'
    elif found_font.lower().find('semibold') > -1:
        new_weight = 'SemiBold'
    elif found_font.lower().find('light') > -1:
        new_weight = 'Light'
    elif found_font.lower().find('regular') > -1:
        new_weight = 'Regular'

    # styles
    elif found_font.lower().find('italic') > -1:
        new_style = 'Italic'
    elif found_font.lower().find('oblique') > -1:
        new_style = 'Oblique'
    elif found_font.lower().find('normal') > -1:
        new_style = 'Normal'
    else:
        something = False

    weight_style = new_weight+new_style
    if weight_style == '':
        weight_style = 'Regular'

    font_to_replace.style = weight_style
    return font_to_replace

#———————————————————————————————————————— fin
