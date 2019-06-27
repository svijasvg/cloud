#---------------------------------------- svg.py
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
#---------------------------------------- program

import os, re, io
from svija.models import Font
from django.core.exceptions import ObjectDoesNotExist

# given path to source file & name (need to figure out what to pass exactly)

def clean(svg_source, svg_name):

    # if unspecified, ID will be filename with languager & extension removed (-en.svg)
    svg_ID = svg_name[:-7]

    svg_source = os.path.abspath(os.path.dirname(__name__)) + '/' + svg_source + '/' + svg_name

    #------------------------------------- initialize values

    width = 0
    height = 0
    line_number = -1
    result = ''
    fonts_found = []
    fonts_woff = []
    fonts_goog = []

    #------------------------------------- list of woff & google fonts

    fonts = Font.objects.all()
    for this_font in fonts:
        if this_font.google:
            fonts_goog.append(this_font)
        else:
            fonts_woff.append(this_font)

    #------------------------------------- read contents of SVG, split into lines

    with open(svg_source, 'r', encoding='utf-8') as f:
        raw_svg = f.read()
        svg_lines = raw_svg.split('\n')

    #------------------------------------- process the SVG line by line

    while True:

        line_number = line_number + 1
        if line_number == len(svg_lines): break # we're done
        line = svg_lines[line_number - 1]

        #---------------------------------- if the AI xml header is there delete it

        if line[0:5] == '<?xml': continue
        if line[0:4] == '<!--': continue

        #-------------------------------- if already ID don't need new ID

        if line[0:4] == '<svg':
            if line.find('id="') > 0:
                svg_ID = ''

        #-------------------------------- remove pixel dimensions if any

        if line[2:9] == 'viewBox':

            #------------------------------ remove pixel dimensions if any

            if line.find('px" ') > 0:
                parts = line.split('px" ')
                line = '\t ' + parts[-1]

            #------------------------------ extract dimensions from viewBox

            parts = line.split('"')
            viewBox = parts[1]
            dimensions = viewBox.split(' ')
            px_width = float(dimensions[2])
            px_height = float(dimensions[3])

        #---------------------------------- replace style definitions
        #---------------------------------- .st10 creates conflict when multiple svg's on a page
        #---------------------------------- replaced with .st[SVG ID]10

        if line[1:4] == '.st':
            parts = line.split('.st')
            line = '\t.st' + svg_ID + parts[1]

            #----- find fonts
            #----- .st24{font-family:'Roboto-Light';}
            if line.find('font-family') > 0:
                line_parts = line.split("'")
                found_font = line_parts[1]
                google_font = [x for x in fonts_goog if x.name == found_font]

                # if it's not one of the google fonts in DB
                if len(google_font) <= 0:
#                    if found_font.find('italic') > -1:
#                        sty = 'Italic'
#                    elif found_font.find('oblique') > -1:
#                        sty = 'Oblique'
#                    elif found_font.find('normal') > -1:
#                        sty = 'Normal'
#                    elif found_font.find('normal') > -1:
#                    else:
                    fonts_found.append(found_font)

                # if it's one of the google fonts in DB
                else:
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

        #---------------------------------- replace style applications
        # class= st2 › staccueil_fr2

        if line.find('class="st') > 0:
            line = re.sub(r'([\"," "])st([0-9]*)(?=[\"," "])', r'\1st'+svg_ID+r'\2', line)

        #---------------------------------- get id if specified

        if line[1:10] == 'g id="id_': svg_ID = line[10:-2]

     #---------------------------------- print this line

        result += '\n' + line;

  #----------------------------------------- add new ID if necessary

    if svg_ID != '':
        result = result.replace('<svg ', '<svg id="' + svg_ID + '" ', 1)

  #----------------------------------------- check font table
  # https://stackoverflow.com/questions/14676613/how-to-import-google-web-font-in-css-file

    for font_name in fonts_found:
        try:
            font_obj = Font.objects.get(name = font_name)
            rien = 0
        except ObjectDoesNotExist:
            p = Font.objects.create(name = font_name, family='', style='', google= False, active = False)
            p.save

    return svg_ID, px_width, px_height, result

  #----------------------------------------- fin
