#———————————————————————————————————————— get_fonts.py
# should be first in CSS
# by default all fonts are included
# svg_cleaner adds fonts only if they're not already in DB

from svija.models import Font

#ef get_fonts(core_content):
def get_fonts():
    font_objs = Font.objects.all()
    css_str  = "@font-face {{ font-family:'{}'; src:{}'){}; }}"
    link_str = '\n  <link rel="stylesheet" href="{}" />'
    font_css = ''
    google_fonts = []
    font_link = ''

    for this_font in font_objs:
        if this_font.active:
            font_face = this_font.css
            font_src  = this_font.source

            if this_font.google:
                req = this_font.style.lower().replace(' ','')
                req = this_font.family.replace(' ','+') + ':' + req 
                google_fonts.append(req)

            elif font_src.find('woff2') > 0:
                font_format = " format('woff2')"
                font_src = "url('/fonts/" + font_src
                font_css  += '\n'+ css_str.format(font_face, font_src, font_format)

            elif font_src.find('woff') > 0:  
                font_format = " format('woff')"
                font_src = "url('/fonts/" + font_src
                font_css += '\n'+ css_str.format(font_face, font_src, font_format)

            elif font_src.find(',') > 0: # local fonts
                # src: local('Arial'), local('Arial MT'), local('Arial Regular'); }
                font_format = ''
                locals = font_src.replace(', ',',').split(',')
                font_src = "local('"+"'), local('".join(locals)
                font_css += '\n'+ css_str.format(font_face, font_src, font_format)


    if len(google_fonts) > 0:
        link_str = '  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family={}">'
        font_link = link_str.format(('|').join(google_fonts))

    #ore_content['meta_fonts'] = font_link
    #ore_content['css'] = font_css + core_content['css']
    #eturn core_content
    return font_link, font_css
