
#:::::::::::::::::::::::::::::::::::::::: get_font_css.py

#———————————————————————————————————————— notes
#
#   fonts are added to DB in svg_cleaner.py
#
#   this manages them AFTER they've been added
#   it creates three things:
#
#   1. meta link to google fonts
#   2. css for woff fonts
#   3. css for adobe fonts
#
#   The last two are combined (no reason to send
#   them separately)
#
#   there is ALSO CSS in the SVG source
#
#   should be first in CSS
#   by default all fonts are included
#
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

#———————————————————————————————————————— generate woff CSS

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

  if woff_css != '': woff_css += '\n'

#———————————————————————————————————————— generate adobe css
#
#    separate from earlier loop because all adobe fonts are combined
#    into a single CSS block, with only one copyright comment section
#
#   <link rel="stylesheet" href="https://use.typekit.net/ycw1wbc.css">

  adobe_css = ''

  # get comments from first font in list
  if len(adobe_fonts) > 0:
    adobe_css  = '/* adobe font css */\n\n'
    adobe_css += first_comment(adobe_fonts[0].adobe_sheet)

  
  for this_font in adobe_fonts:
    family = "font-family: '"+this_font.family + "'; "
    weight = "font-weight: " + this_font.weight + "; "
    style  = "font-style: " + this_font.style + "; "
    url    = "src:url("+this_font.adobe_url+") format('woff2');"
    adobe_css += "\n@font-face { " + family + weight + style + url + " }"
  if adobe_css != '':
    adobe_css += '\n'

#———————————————————————————————————————— generate google font link & css

  google_link = make_google_link(google_fonts)


  return google_link, woff_css + adobe_css

#:::::::::::::::::::::::::::::::::::::::: main method

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


#:::::::::::::::::::::::::::::::::::::::: utility methods

#———————————————————————————————————————— first_comment(css)

def first_comment(css):
  start = css.find('/*\n')
  end   = css.find('"}*/\n') + 4
  return css[start:end] + '\n'


#:::::::::::::::::::::::::::::::::::::::: fin

