
#:::::::::::::::::::::::::::::::::::::::: get_font_css.py

#———————————————————————————————————————— notes
#
#   fonts are added to DB in svg_cleaner.py
#
#   this manages them AFTER they've been added
#
#   should be first in CSS
#   by default all fonts are included
#   svg_cleaner adds fonts only if they're not already in DB
#  
#   if there's a global list of fonts in PageView
#   svg cleaner can add to it
#   and this function can use it IF it's after svg cleaner
#
#———————————————————————————————————————— imports

from svija.models import Font
import requests
from django.db.models import Q


#:::::::::::::::::::::::::::::::::::::::: main definition

def get_font_css():

#———————————————————————————————————————— set up arrays

  woff_fonts   = Font.objects.filter(enabled=True).exclude(woff='')
  adobe_fonts  = Font.objects.filter(enabled=True).exclude(adobe_pasted='')
  google_fonts = Font.objects.filter(Q(enabled=True) & Q(google = True)).order_by('family')
  google_link  = ''

#———————————————————————————————————————— loop through woff fonts

  woff_css = ''

  empty_woff   = "@font-face {{ font-family:'{}'; src:{}'){}; }}"

  for this_font in woff_fonts:
    woff = this_font.woff
    svg_ref = this_font.svg_ref

    if woff.find(',') > 0: # local fonts
      font_format = ''
      locals = woff.replace(', ',',').split(',')
      woff = "local('" + ("'), local('".join(locals))
      woff_css += '\n'+ empty_woff.format(svg_ref, woff, font_format)
      continue

    elif woff.find('woff2') > 0: # woff2 format
      font_format = " format('woff2')"
      woff_url = "url('/fonts/" + woff
      woff_css  += '\n'+ empty_woff.format(svg_ref, woff_url, font_format)
      continue

    elif woff.find('woff') > 0: # woff format
      font_format = " format('woff')"
      woff_url = "url('/fonts/" + woff
      woff_css += '\n'+ empty_woff.format(svg_ref, woff_url, font_format)
      continue


    else:
      this_font.woff = ''
      this_font.save()

#———————————————————————————————————————— generate adobe css
#
#    separate from earlier loop because all adobe fonts are combined
#    into a single CSS block, with only one copyright comment section

  adobe_css = ''

  # get comments from first font in list
  if len(adobe_fonts) > 0:
    adobe_css = first_comment(adobe_fonts[0].adobe_sheet)
  
  for this_font in adobe_fonts:
      adobe_css += "\n@font-face { font-family:'"+this_font.svg_ref + "'; src:url("+this_font.adobe_url+") format('woff2'); }"

#———————————————————————————————————————— generate google font link & css

  google_link = make_google_link(google_fonts)
  google_css  = make_google_css(google_fonts)


  return google_link, woff_css + adobe_css + google_css

#:::::::::::::::::::::::::::::::::::::::: main methods

#———————————————————————————————————————— make_google_link(google_fonts)

#   https://developers.google.com/fonts/docs/getting_started
#   https://fonts.googleapis.com/css?family=Cantarell:i|Droid+Serif:700
#                                           fontName:400,500,500italic|fontName

def make_google_link(google_fonts):
  if len(google_fonts) == 0: return ''

  this_family    = google_fonts[0].family.replace(' ', '+')
  finished_fonts = [this_family+':']
  separator      = ''

  for font in google_fonts:
    family = font.family.replace(' ', '+')
    weight = font.weight
    style  = font.style

    if family != this_family:
      this_family = family
      finished_fonts.append(this_family+':')
      separator = ''

    finished_fonts[len(finished_fonts)-1] += separator + weight + style
    separator = ','

  src = '|'.join(finished_fonts)
  return '  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=' + src + '">\n'

#———————————————————————————————————————— make_google_css(google_fonts)

#   previously, there was no google_css per se
#   instead, the style declarations were put in
#   the SVG styles, inside the SVG files

#   this time, I would like to move them to a block at
#   the top of the page

#   @font-face { font-family:'Khand-Medium'; src:url('/fonts/Khand-Medium.woff') format('woff'); }

# .stsvg_Font-Test0{fill:#FFFFFF;fill:color(display-p3 1.0 1.0 1.0);;}
# .stsvg_Font-Test1{fill:#333333;fill:color(display-p3 0.2 0.2 0.2);;}
# .stsvg_Font-Test2{font-family:'OpenSans-Light';}
# .stsvg_Font-Test3{font-size:15px;}
# .stsvg_Font-Test4{font-family:'OpenSansLight-Italic';}
# .stsvg_Font-Test5{font-family:'OpenSans';}
# .stsvg_Font-Test6{font-family:'OpenSans-Italic';}
# .stsvg_Font-Test7{font-family:'OpenSans-Semibold';}
# .stsvg_Font-Test8{font-family:'OpenSans-SemiboldItalic';}
# .stsvg_Font-Test9{font-family:'OpenSans-Bold';}
# .stsvg_Font-Test10{font-family:'OpenSans-BoldItalic';}
# .stsvg_Font-Test11{font-family:'OpenSans-Extrabold';}
# .stsvg_Font-Test12{font-family:'OpenSans-ExtraboldItalic';}
# .stsvg_Font-Test13{font-family:'Poppins-Thin';}
# .stsvg_Font-Test14{font-family:'Poppins-ThinItalic';}
# .stsvg_Font-Test15{font-family:'Poppins-ExtraLight';}
# .stsvg_Font-Test16{font-family:'Poppins-ExtraLightItalic';}
# .stsvg_Font-Test17{font-family:'Poppins-Light';}
# .stsvg_Font-Test18{font-family:'Poppins-LightItalic';}
# .stsvg_Font-Test19{font-family:'Poppins-Regular';}
# .stsvg_Font-Test20{font-family:'Poppins-Italic';}
# .stsvg_Font-Test21{font-family:'Poppins-Medium';}
# .stsvg_Font-Test22{font-family:'Poppins-MediumItalic';}
# .stsvg_Font-Test23{font-family:'Poppins-SemiBold';}
# .stsvg_Font-Test24{font-family:'Poppins-SemiBoldItalic';}
# .stsvg_Font-Test25{font-family:'Poppins-Bold';}
# .stsvg_Font-Test26{font-family:'Poppins-BoldItalic';}
# .stsvg_Font-Test27{font-family:'Poppins-ExtraBold';}
# .stsvg_Font-Test28{font-family:'Poppins-ExtraBoldItalic';}
# .stsvg_Font-Test29{font-family:'Poppins-Black';}
# .stsvg_Font-Test30{font-family:'Poppins-BlackItalic';}

#   @font-face {
#       font-family: 'openSans-Bold';
#       src: url('OpenSans-Bold-webfont.eot');
#       src: url('OpenSans-Bold-webfont.eot?#iefix') format('embedded-opentype'),
#            url('OpenSans-Bold-webfont.woff') format('woff'),
#            url('OpenSans-Bold-webfont.ttf') format('truetype'),
#            url('OpenSans-Bold-webfont.svg#openSans-Bold') format('svg');
#       font-weight: normal;
#       font-style: normal;
#   }


#   https://stackoverflow.com/a/4760881/72958

def make_google_css(google_fonts):
  if len(google_fonts) == 0: return ''

  actual_fonts = []
  font_vars    = []

  for font in google_fonts:

    svg    = font.svg_ref
    family = font.family
    weight = font.weight
    style  = font.style

    #————— using vars to redirect to google 
    this  = '\n--' + svg + ': '
    this += '"' + family + '"'
    font_vars.append(this)

    #————— main declarations for SVG references
    this  = 'font-family: var(--' + svg+ '); '
    this += 'font-weight: ' + weight + ';'
    this += 'font-style: ' + style  + '; }'
    this  = '@font-face { '+this

    actual_fonts.append(this)

  srx = '\n:root{ ' + ';'.join(font_vars) + '\n}'
  src = '\n'.join(actual_fonts)

  return '/* Google fonts */\n' + srx + '\n\n' + src + '\n'

#   https://stackoverflow.com/questions/48353458/can-one-alias-multiple-font-names-with-a-single-name-in-css
# I can use the "root" thing to redirect the SVG names to the real names


#:::::::::::::::::::::::::::::::::::::::: utility methods

#———————————————————————————————————————— first_comment(css)

def first_comment(css):
  start = css.find('/*\n')
  end   = css.find('"}*/\n') + 4
  return css[start:end] + '\n'


#:::::::::::::::::::::::::::::::::::::::: fin

