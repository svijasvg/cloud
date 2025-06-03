
#:::::::::::::::::::::::::::::::::::::::: integrate_fonts.py

#———————————————————————————————————————— notes
#
#   fonts are added to DB in rewrite_svg.py
#   the first time a page requires new fonts
#
#   the method below fleshes out the family,
#   weight and style
#
#———————————————————————————————————————— imports

from django.db.models import Q
from svija.models import Font
import requests


#:::::::::::::::::::::::::::::::::::::::: main definition

def integrate_fonts():

#:::::::::::::::::::::::::::::::::::::::: WHILE DEBUGGING

  all_fonts = Font.objects.filter(enabled=True)
  for this_font in all_fonts:
    this_font.adobe_pasted = '<link rel="stylesheet" href="https://use.typekit.net/jpl1zaz.css">'
    this_font.save()
#   <link rel="stylesheet" href="https://use.typekit.net/aav4onz.css">

#———————————————————————————————————————— remove conflicts
#
#   if google is checked, can't add adobe or woff
#   if woff is filled out, can't add adobe
#
#   google > woff > adobe

  all_fonts = Font.objects.filter(enabled=True)

  for this_font in all_fonts:
    if this_font.google and this_font.woff != '':
      this_font.woff = ''
      this_font.save()
      
    if this_font.google and this_font.adobe_pasted != '': # worked
      this_font.adobe_pasted = ''
      this_font.adobe_url    = ''
      this_font.adobe_sheet  = ''
      this_font.save()
      
    if this_font.woff != '' and this_font.adobe_pasted != '': # worked
      this_font.adobe_pasted = ''
      this_font.adobe_url    = ''
      this_font.adobe_sheet  = ''
      this_font.save()

#———————————————————————————————————————— initialize arrays WOFF & GOOGLE COMMENTED OUT ALL FONTS ARE ADOBE

#   I don't want to mess with information that may have been manualy modified


  adobe_fonts  = Font.objects.filter(Q(enabled=True) & Q(adobe_sheet='')).exclude(adobe_pasted='')

# woff_fonts   = Font.objects.filter(enabled=True).exclude(woff='')
# google_fonts = Font.objects.filter(
#                  Q(enabled = True ) &
#                  Q(google  =  True) &
#                 (Q(family  = ''   ) | Q(weight='') | Q(style=''))
#                )

#———————————————————————————————————————— ▼ get Adobe stylesheets
#
#   <link rel="stylesheet" href="https://use.typekit.net/jpl1zaz.css">

#   there will only be a few different CSS sheets for Adobe Fonts —
#   normally, there will only be one.
#   
#   So I'm better off flooping through the fonts, and getting the
#   corret stylesheet into a dict, with the Adobe ID as the index
#   and a list of associated fonts & URLS
#   
#   otherwise I'm duplicationg work for each font that doesn't have to be done

#   in admin.py:
#   return obj.adobe_pasted[53:60]

#   <link rel="stylesheet" href="https://use.typekit.net/jpl1zaz.css">      svija.dev
#   <link rel="stylesheet" href="https://use.typekit.net/aav4onz.css">  alt.svija.dev (1 font)

  adobe_sheets     = {}
  adobe_font_lists = {}

  for this_font in adobe_fonts:

#———————————————————————————————————————— verify pasted format & length

#   <link rel="stylesheet" href="https://use.typekit.net/jpl1zaz.css">

    if this_font.adobe_pasted[0:22] != '<link rel="stylesheet"':
      this_font.adobe_url = "⚠️ Pasted link is wrong format"
      this_font.adobe_sheet = this_font.adobe_pasted[0:22]
      this_font.save()

#     del this_font
      continue

    if len(this_font.adobe_pasted) != 66:
      this_font.adobe_url = "⚠️ Pasted link is wrong length"
      this_font.adobe_sheet = this_font.adobe_pasted
      this_font.save()

#     del this_font
      continue

#———————————————————————————————————————— it it's already treated, continue

    adobe_id = this_font.adobe_pasted[53:60]

    if adobe_id in adobe_sheets: continue

#———————————————————————————————————————— get associated CSS file

    css_str = css_file_from_tag(this_font.adobe_pasted) # worked

#———————————————————————————————————————— if empty, skip

    if css_str == '':
      this_font.adobe_url = '⚠️ Pasted link returned wrong content'
      this_font.adobe_sheet = ''
      this_font.save()

      # remove this_font from adobe_fonts
      continue

#———————————————————————————————————————— ▲ get font list from file

    adobe_sheets[adobe_id]     = css_str
    adobe_font_lists[adobe_id] = fonts_from_adobe_sheet(css_str)


#:::::::::::::::::::::::::::::::::::::::: font info

#———————————————————————————————————————— ▼ get font url for each Adobe font

  for this_font in adobe_fonts:

#———————————————————————————————————————— get font url and save css sheet SHEET SAVING COMMENTED OUT

    adobe_id  = this_font.adobe_pasted[53:60]
    font_list = adobe_font_lists[adobe_id]
    this_font = adobe_font_from_list(this_font, font_list) 

    if this_font.adobe_url == '':
      this_font.category = '⚠️ no match found' 
      this_font.adobe_url = '⚠️ search CSS manually'

#   this_font.adobe_sheet = adobe_sheets[adobe_id]
    this_font.save()

#———————————————————————————————————————— ▲ end loop and exit

  return True


#:::::::::::::::::::::::::::::::::::::::: legacy code

#———————————————————————————————————————— add new Adobe fonts
#
#   <link rel="stylesheet" href="https://use.typekit.net/jpl1zaz.css">
#
#   right now, the Adobe stylesheet is parsed again for each new font
#   but generally, there will only be one stylesheet for a site
# 
#   so I could keep the contents and reuse it for each font
#   but I need a way to track which sheets were integrated
#   so that if someone uses two different adobe sheets
#   it will still work
#
#   web project for dev.svija.love
#   <link rel="stylesheet" href="https://use.typekit.net/ycw1wbc.css">


  for this_font in adobe_fonts:

    break

    # check for valid link
    if this_font.adobe_pasted[0] != '<':   # contents is not "<link rel..."
      this_font.adobe_url = "⚠️ Error in pasted link"
      this_font.adobe_sheet = ''
      this_font.save()
      continue

    this_font.adobe_url = "⚠️  DEBUG INFO"
    debug_str = ''
    for x_font in font_list:
      debug_str += x_font
    this_font.adobe_sheet = stylesheet
    this_font.save()

    # get list of fonts in stylesheet
    font_list, stylesheet = font_list_from_link(this_font.adobe_pasted)

    if type(font_list) is str:
      this_font.adobe_url = font_list
      this_font.adobe_sheet = ''
      this_font.save()
      continue

    # convert svg ref to [family, weight and style]
    target_font = interpret_adobe(this_font.svg_ref) # family:eight, weight:600, style:normal

    # find match between target_font and font_list
    font = best_adobe_match(target_font, font_list)

    # if match failed
    if type(font) is str:
      this_font.adobe_url = font
      this_font.adobe_sheet = stylesheet
      this_font.save()
      continue

    # all is good so save info
    if this_font.family == '':
      this_font.family      = font['family']
    if this_font.weight == '':
      this_font.weight      = font['weight']
    if this_font. style == '':
      this_font.style       = font['style']

    this_font.adobe_url   = font['url']
    this_font.adobe_sheet = stylesheet

    this_font.save()


#———————————————————————————————————————— COMMENTED OUT add new WOFF fonts
#
#   this just means cleaning up path if someone
#   dragged it from the finder

# for this_font in woff_fonts:

#   # remove everything in beginning of path if necessary
#   # /Users/Main/Library/Mobile Documents/com~apple~CloudDocs/Desktop/svija.dev/SYNC/SVIJA/Fonts/Woff Files/clarendon.woff

#   woff = this_font.woff
#   if woff.find('/') > -1:
#     woff = woff.rpartition("/")[2]
#     this_font.woff = woff
#     this_font.save()

#———————————————————————————————————————— add new Google fonts COMMENTED OUT

#   this is seemingly unnecessary — all the necessary information is already
#   supplied via the SVG code

#   https://tech.svija.com/reference/fonts/google-fonts

# for this_font in google_fonts:

#   font = interpret_google(this_font.svg_ref)
#   if this_font.family == '':
#     this_font.family      = font['family']
#   if this_font.weight == '':
#     this_font.weight      = font['weight']
#   if this_font. style == '':
#     this_font.style       = font['style']

#   this_font.save()


  return True

#:::::::::::::::::::::::::::::::::::::::: google-related methods

#———————————————————————————————————————— interpret_google(svg_ref)

#   if it's google, we search for one of the weights and
#   split on it, then use family + weight + rest (style),
#   with slashes changed to single spaces
#   style is optional

#   font-family: 'Open Sans';
#   font-style: normal;
#   font-weight: 300;
#   font-stretch: 100%;
#   font-display: swap;
#   src: url(https://fonts.gstatic.com/s/opensans/v35/memSYaGs126MiZpBA-UvWbX2vVnXBbObj2OVZyOOSr4dVJWUgsiH0B4taVQUwaEQbjB_mQ.woff) format('woff');
#   unicode-range: U+0460-052F, U+1C80-1C88, U+20B4, U+2DE0-2DFF, U+A640-A69F, U+FE2E-FE2F;

google_weights = {
  'Extralight' : '200',
  'Extra-Light': '200',
  'Semibold'   : '600',
  'Semi-Bold'  : '600',
  'Extrabold'  : '800',
  'Extra-Bold' : '800',
  'Thin'       : '100',
  'Light'      : '300',
  'Regular'    : '400',
  'Medium'     : '500',
  'Bold'       : '700',
  'Black'      : '900',
  'default'    : '400',
}

google_styles = {
  'Cond'       : 'condensed',
  'Oblique'    : 'italic',
  'Obl'        : 'italic',
  'Italic'     : 'italic',
  'default'    : 'normal',
}

def interpret_google(svg_ref):

  # need to replace ExtraBlack with Extrablack — why? don't remember
  svg_ref = fix_caps(svg_ref)

  raw_string = add_dashes(svg_ref)

  parts = raw_string.split('-')
  parts[0] = convert_number_to_word(parts[0]) # fix for a font called "8"

# start at end of string, and if it's either a weight or a style
# we keep going

  family = weight = style = ''

  # range(start, stop, step)
  for part in range(len(parts)-1, -1, -1):
    this_part = parts[part]

    if this_part in google_weights:
      weight = google_weights[this_part]
      parts.pop() # remove last element
      continue

    if this_part in google_styles:
      style = google_styles[this_part]
      parts.pop() # remove last element
      continue

    break

  family = ' '.join(parts) 

  if style == '':
    style = google_styles['default']

  if weight == '':
    weight = google_weights['default']

  return {'family':family, 'weight':weight, 'style':style, }


#:::::::::::::::::::::::::::::::::::::::: main adobe method

#———————————————————————————————————————— adobe_font_from_list(this_font, candidates) 

# 8-Heavy doesn't work, though everything seems to be correct

def adobe_font_from_list(this_font, font_list):

# tag needs to be what line was triggered

#———————————————————————————————————————— simplified values for testing

  test_svg_ref = simplified(this_font.svg_ref)
  test_family  = simplified(this_font.family )
  test_weight  = simplified(this_font.weight )
  test_style   = simplified(this_font.style  )

  if test_weight == '': test_weight = derive_adobe_weight(this_font)
  if test_style  == '': test_style  = derive_adobe_style(this_font)
  if test_style  == 'oblique': test_style = 'italic'

  if test_weight == '': test_weight = '400'
  if test_style  == '': test_style  = 'normal'

#———————————————————————————————————————— weight & style match • svg ref matches candidate family

  for x in range(len(font_list)):
    candidate = font_list[x]
    if test_weight == candidate['weight'] and test_style == candidate['style']:

      if test_svg_ref == candidate['family']: #################################
        if this_font.weight == '': this_font.weight = test_weight
        if this_font.style  == '': this_font.style  = test_style
        this_font.adobe_url = candidate['url']

        this_font.category = 'WS-SVG ref'
        debug  = 'svg: ' + test_svg_ref +':'+ test_family +':'+ test_weight +':'+ test_style+'\n'
        debug += 'sheet: ' + candidate['family'] +':'+ candidate['weight'] +':'+ candidate['style']
        this_font.adobe_sheet = debug
        return this_font

#———————————————————————————————————————— weight & style match • test family matches candidate family

  for x in range(len(font_list)):
    candidate = font_list[x]

    if test_weight == candidate['weight'] and test_style == candidate['style']:

      if test_family == candidate['family']: #################################
        if this_font.weight == '': this_font.weight = test_weight
        if this_font.style  == '': this_font.style  = test_style
        this_font.adobe_url = candidate['url']

        this_font.category = 'WS-family'
        debug  = 'svg: ' + test_svg_ref +':'+ test_family +':'+ test_weight +':'+ test_style+'\n'
        debug += 'sheet: ' + candidate['family'] +':'+ candidate['weight'] +':'+ candidate['style']
        this_font.adobe_sheet = debug
        return this_font

#———————————————————————————————————————— style matches • svg_ref matchs candidate family

  for x in range(len(font_list)):
    candidate = font_list[x]
    if test_style == candidate['style']:

      if test_svg_ref == candidate['family']: #################################
        if this_font.weight == '': this_font.weight = test_weight
        if this_font.style  == '': this_font.style  = test_style
        this_font.adobe_url = candidate['url']

        this_font.category = 'S-SVG ref'
        debug  = 'svg: ' + test_svg_ref +':'+ test_family +':'+ test_weight +':'+ test_style+'\n'
        debug += 'sheet: ' + candidate['family'] +':'+ candidate['weight'] +':'+ candidate['style']
        this_font.adobe_sheet = debug
        return this_font

#———————————————————————————————————————— weight matches • svg ref matches candidate family

  for x in range(len(font_list)):
    candidate = font_list[x]
    if test_weight == candidate['weight']:

      if test_svg_ref == candidate['family']:
        if this_font.weight == '': this_font.weight = test_weight
        if this_font.style  == '': this_font.style  = test_style
        this_font.adobe_url = candidate['url']

        this_font.category = 'W-SVG-ref'
        debug  = 'svg: ' + test_svg_ref +':'+ test_family +':'+ test_weight +':'+ test_style+'\n'
        debug += 'sheet: ' + candidate['family'] +':'+ candidate['weight'] +':'+ candidate['style']
        this_font.adobe_sheet = debug
        return this_font

#———————————————————————————————————————— weight matches • test family matchs candidate family

  for x in range(len(font_list)):
    candidate = font_list[x]
    if test_weight == candidate['weight']:

      if test_family == candidate['family']:
        if this_font.weight == '': this_font.weight = test_weight
        if this_font.style  == '': this_font.style  = test_style
        this_font.adobe_url = candidate['url']

        this_font.category = 'W-family'
        debug  = 'svg: ' + test_svg_ref +':'+ test_family +':'+ test_weight +':'+ test_style+'\n'
        debug += 'sheet: ' + candidate['family'] +':'+ candidate['weight'] +':'+ candidate['style']
        this_font.adobe_sheet = debug
        return this_font

#———————————————————————————————————————— style matches • test family matchs candidate family SHOULD MATCH 8-HEAVY

  for x in range(len(font_list)):
    candidate = font_list[x]
   
    if test_style == candidate['style']:

      if test_family == candidate['family']:
        if this_font.weight == '': this_font.weight = test_weight
        if this_font.style  == '': this_font.style  = test_style
        this_font.adobe_url = candidate['url']

        this_font.category = 'S-family'
        debug  = 'svg: ' + test_svg_ref +':'+ test_family +':'+ test_weight +':'+ test_style+'\n'
        debug += 'sheet: ' + candidate['family'] +':'+ candidate['weight'] +':'+ candidate['style']
        this_font.adobe_sheet = debug
        return this_font

#———————————————————————————————————————— svg ref matches candidate family

  for x in range(len(font_list)):
    candidate = font_list[x]
    if test_svg_ref == candidate['family']: ####################################
      if this_font.weight == '': this_font.weight = test_weight
      if this_font.style  == '': this_font.style  = test_style
      this_font.adobe_url = candidate['url']

      this_font.category = 'SVG ref'
      debug  = 'svg: ' + test_svg_ref +':'+ test_family +':'+ test_weight +':'+ test_style+'\n'
      debug += 'sheet: ' + candidate['family'] +':'+ candidate['weight'] +':'+ candidate['style']
      this_font.adobe_sheet = debug
      return this_font

#———————————————————————————————————————— test family matches candidate family

  for x in range(len(font_list)):
    candidate = font_list[x]
    if test_family == candidate['family']: ####################################
      if this_font.weight == '': this_font.weight = test_weight
      if this_font.style  == '': this_font.style  = test_style
      this_font.adobe_url = candidate['url']

      this_font.category = 'family'
      debug  = 'svg: ' + test_svg_ref +':'+ test_family +':'+ test_weight +':'+ test_style+'\n'
      debug += 'sheet: ' + candidate['family'] +':'+ candidate['weight'] +':'+ candidate['style']
      this_font.adobe_sheet = debug
      return this_font

#———————————————————————————————————————— ▲ end loop and exit

  this_font.adobe_url = ''
  return this_font


#   can these be fixed manually? How? Document it!

#   font families with problems caused by Adobe's incoherence
#   displays correctly; CSS gives wrong weight:
#   if I can detect the problem, I can fix it by overriding weight

#     svg: futuraptdemi:futurapt:300:normal
#   sheet: futurapt:300:normal
#     svg: futuraptdemiobl:futurapt:300:italic
#   sheet: futurapt:300:italic
#     svg: futuraptheavy:futurapt:800:normal
#   sheet: futurapt:800:normal
#     svg: futuraptheavyobl:futurapt:800:italic
#   sheet: futurapt:800:italic
#     svg: futuraptextrabold:futurapt:700:normal
#   sheet: futurapt:700:normal
#     svg: futuraptextraboldobl:futurapt:700:italic
#   sheet: futurapt:700:italic
#   svg: proximanovatthin:proximanova:200:normal
#   sheet: proximanova:900:normal
#   svg: proximanovablack:proximanova:800:normal
#   sheet: proximanova:800:normal

#   woff2 file is just not the same as the installed Illustrator file
#   the problem is that Adobe defines both Futura PT Bold and Futura PT Heavy as 700 weight

#   svg: futuraptboldobl:futurapt:700:oblique SHOULD MATCH WEIGHT STYLE & FAMILY
#   sheet: futurapt:700:normal

#———————————————————————————————————————— temporary notes

# svg ref: FolkRoughOT
# svg fam: Folk Rough OT
# adb css: ff-folk-rough


#:::::::::::::::::::::::::::::::::::::::: adobe-related secondary methods

#———————————————————————————————————————— fonts_from_adobe_sheet(css_str)
#
#   extracts fonts from and Adobe typekit CSS sheet
#
#   https://use.typekit.net/jpl1zaz.css?lkjsdlmkqsd
#
#   returns a list of font dictionaries with
#   family, weight, style and woff2 src URL

def fonts_from_adobe_sheet(css_str):
  css_str = css_str.split('@font-face', 1)[1]
  css_str = css_str.split('\n\n.tk-', 1)[0]

  font_list = []
  blocks    = css_str.split('@font-face')

  for block in blocks:
    lines   = block.split('\n')

    ffamily = simplified(lines[1][13:-2])
    furl    = lines[2].split('"')[1]

    finfo   = lines[3][29:-21]
    fstyle  = simplified(finfo.split(';')[0])
    fweight = simplified(finfo.split(':')[1])

    font = {'family': ffamily, 'weight': fweight, 'style': fstyle, 'url':furl}
    font_list.append(font)

  return font_list

#———————————————————————————————————————— find_font_in_sheet(this_font, css_sheet) 

def find_font_in_sheet(this_font, css_sheet):
  return 'find_font_in_sheet()'

#———————————————————————————————————————— derive_adobe_style(font)

adobe_styles = {
  'oblique'   : 'italic',
  'obl'       : 'italic',
  'italic'    : 'italic',
  'book'      : 'normal',
}

def derive_adobe_style(font):

  svg_name   = font.svg_ref.lower()
  old_style = font.style
  new_style = ''

  for this_style in adobe_styles.keys():
    if this_style in svg_name:
      new_style = adobe_styles[this_style]
      break

  if new_style != '': return new_style
  if old_style != '': return old_style
  return 'normal'

#———————————————————————————————————————— derive_adobe_weight(font, adobe_weights)

adobe_weights = {
  'extralight' : '200',
  'extra-light': '200',
  'extrabld'   : '800',
  'extrabold'  : '800',
  'extra-bld'  : '800',
  'extra-bold' : '800',
  'semibold'   : '600',
  'semi-bold'  : '600',
  'ultrablack' : '900',
  'ultra-black': '900',
  'demi'       : '600',
  'thin'       : '100',
  'light'      : '300',
  'book'       : '400',
  'regular'    : '400',
  'heavy'      : '700',
  'medium'     : '500',
  'bold'       : '700',
  'black'      : '900',
  'default'    : '',
}

def derive_adobe_weight(font):

  svg_name   = font.svg_ref.lower()
  old_weight = font.weight
  new_weight = ''

  for this_weight in adobe_weights.keys():
    if this_weight in svg_name:
      new_weight = adobe_weights[this_weight]
      break

  if new_weight != '': return new_weight
  if old_weight != '': return old_weight
  return '400'

#———————————————————————————————————————— font_list_from_css(this_font)

#   accepts css sheet from pasted adobe link
#
#   returns array of fonts found in css string
#
#   returned fonts are dictionaries
#   - family: family name
#   - woff2 : woff source URL
#   - style : style
#   - weight: number

# upper or lower?

def font_list_from_css(stylesheet):

  #———————————————————————————————————————— initialize

  font_list = []
  start_index = 0

  how_many = int(stylesheet.count('font-face'))

  for x in range(how_many):

    #———————————————————————————————————— name
  
    name_begin = stylesheet.find('font-family', start_index) + 13
    name_end   = stylesheet.find('"', name_begin)
    name       = stylesheet[name_begin:name_end]
  
    #———————————————————————————————————— url

    url_begin = stylesheet.find('url("', name_end) + 5
    url_end   = stylesheet.find('")', url_begin)
    url       = stylesheet[url_begin:url_end]
  
    #———————————————————————————————————— get style indexes
  
    style_begin = stylesheet.find('font-style:', name_end) + 11
    style_end   = stylesheet.find(';', style_begin)
    style       = stylesheet[style_begin:style_end]
  
    #———————————————————————————————————— get weight indexes
  
    weight_begin = stylesheet.find('font-weight:', name_end) + 12
    weight_end   = stylesheet.find(';', weight_begin)
    weight       = stylesheet[weight_begin:weight_end]
  
    #———————————————————————————————————— add font to list

    font = {'family': name,  'url': url, 'style': style, 'weight': weight,}
    font_list.append(font)
    start_index = style_end


  return font_list

#———————————————————————————————————————— interpret_adobe(svg_ref)

#   in Adobe css, everything is lowercase with slash separators
#
#   if it's adobe, we search for one of the weights and
#   split on it, then use family + weight + rest (style),
#   with slashes changed to single spaces
#   style is optional

# results = ''
# for key in adobe_weights:
#   if txt.find(key) > 0:
#     txt = txt.replace(key, adobe_weights[key])

def interpret_adobe(svg_ref):

  # need to replace ExtraBlack with Extrablack
  svg_ref = fix_caps(svg_ref)

  raw_string = add_dashes(svg_ref)

  parts = raw_string.split('-')
  parts[0] = convert_number_to_word(parts[0]) # fix for a font called "8"

# start at end of string, and if it's either a weight or a style
# we keep going

  family = weight = style = ''

  debug = ''
  # range(start, stop, step)
  for part in range(len(parts)-1, -1, -1):
    this_part = parts[part]

    debug += str(part)+':'+this_part

    if this_part in adobe_weights:
      weight = adobe_weights[this_part]
      parts.pop() # remove last element
      continue

    if this_part in adobe_styles:
      style = adobe_styles[this_part]
      parts.pop() # remove last element
      continue

    break

  family = '-'.join(parts) 

  if style == '':
    style = adobe_styles['default']

  if weight == '':
    weight = adobe_weights['default']

  return {'family':family, 'weight':weight, 'style':style, 'url':''}

#———————————————————————————————————————— font_list_from_link(this_font)

#   accepts pasted adobe link
#
#   returns error string or list of fonts found in css + stylesheet
#
#   returned fonts are arrays:
#   - family: family name
#   - woff2 : woff source URL
#   - style : style
#   - weight: number

#   /* ADOBE CSS FILE CONTENTS
#    * The Typekit service used to deliver this font or fonts for use on websites
#    * is provided by Adobe and is subject to these Terms of Use
#    * http://www.adobe.com/products/eulas/tou_typekit. For font license
#    * information, see the list below.
#    *
#    * abigail:
#    *   - http://typekit.com/eulas/0000000000000000773596e9
#    * acier-bat-gris:
#    *   - http://typekit.com/eulas/00000000000000007735dfaf
#    *
#    * © 2009-2022 Adobe Systems Incorporated. All Rights Reserved.
#    */
#   /*{"last_published":"2022-12-15 08:13:52 UTC"}*/
#   
#   @import url("https://p.typekit.net/p.css?s=1&k=jpl1zaz&ht=tk&f=534.27707&a=24326271&app=typekit&e=css");
#   
#   @font-face {
#   font-family:"abigail";
#   src:url("https://use.typekit.net/af/502479/0000000000000000773596e9/30/l?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n4&v=3") format("woff2"),url("https://use.typekit.net/af/502479/0000000000000000773596e9/30/d?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n4&v=3") format("woff"),url("https://use.typekit.net/af/502479/0000000000000000773596e9/30/a?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n4&v=3") format("opentype");
#   font-display:auto;font-style:normal;font-weight:400;font-stretch:normal;
#   }
#   
#   @font-face {
#   font-family:"acier-bat-gris";
#   src:url("https://use.typekit.net/af/b2b981/00000000000000007735dfaf/30/l?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n4&v=3") format("woff2"),url("https://use.typekit.net/af/b2b981/00000000000000007735dfaf/30/d?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n4&v=3") format("woff"),url("https://use.typekit.net/af/b2b981/00000000000000007735dfaf/30/a?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n4&v=3") format("opentype");
#   font-display:auto;font-style:normal;font-weight:400;font-stretch:normal;
#   }
#   
#   .tk-abigail { font-family: "abigail",sans-serif; }
#   .tk-acier-bat-gris { font-family: "acier-bat-gris",sans-serif; }

def font_list_from_link(pasted_link):

  #———————————————————————————————————————— get file contents

  parts = pasted_link.split('"') # <link rel="stylesheet" href="https://use.typekit.net/jpl1zaz.css">
  stylesheet = file_from_url(parts[3])
  if stylesheet[0:2] != '/*': return '⚠️ Error in pasted link'

  #———————————————————————————————————————— initialise

  font_list = []
  start_index = 0

  how_many = int(stylesheet.count('font-face'))


  for x in range(how_many):

    #———————————————————————————————————— name
  
    name_begin = stylesheet.find('font-family', start_index) + 13
    name_end   = stylesheet.find('"', name_begin)
    name       = stylesheet[name_begin:name_end]
  
    #———————————————————————————————————— url

    url_begin = stylesheet.find('url("', name_end) + 5
    url_end   = stylesheet.find('")', url_begin)
    url       = stylesheet[url_begin:url_end]
  
    #———————————————————————————————————— get style indexes
  
    style_begin = stylesheet.find('font-style:', name_end) + 11
    style_end   = stylesheet.find(';', style_begin)
    style       = stylesheet[style_begin:style_end]
  
    #———————————————————————————————————— get weight indexes
  
    weight_begin = stylesheet.find('font-weight:', name_end) + 12
    weight_end   = stylesheet.find(';', weight_begin)
    weight       = stylesheet[weight_begin:weight_end]
  
    #———————————————————————————————————— add font to list

    font = {'family': name,  'url': url, 'style': style, 'weight': weight,}
    font_list.append(font)
    start_index = style_end


  return font_list, stylesheet

#———————————————————————————————————————— best_adobe_match(target_font, font_list)

#   accepts:
#
#   target_font {family, weight, style}
#   font_list  [{'family': family,  'url': url, 'style': style, 'weight': weight,} ... ]
#   

def best_adobe_match(target_font, font_list):

  family = style = weight = url = ''

  #————— get best family match (breaks for family futura-pt-bold)

  best_match       = 0

  for font in font_list:

    # match at beginning of family name + match at end of family name
    this_match = matching_chars(target_font['family'], font['family'])
    if this_match > best_match:
      best_match = this_match
      family = font['family']

  if best_match == 0: return '⚠️ Font not found in stylesheet'

  #————— get best style match

  best_match  = 0

  for font in font_list:
    if family != font['family']: continue

    this_match = matching_chars(target_font['style'], font['style'])
    if this_match > best_match:
      best_match = this_match
      style = font['style']

  if best_match == 0:  style = ''

  #————— get best weight match

  best_match  = 0

  for font in font_list:
    if family != font['family']: continue
#   if style  != font['style' ]: continue

    this_match = matching_chars(target_font['weight'], font['weight'])

    if this_match > best_match:
      best_match = this_match
      weight = font['weight']

  if best_match == 0: weight = ''

  #————— style if not present find font with same family & weight, and steal style

  if style == '':
    for font in font_list:
      if family != font['family']: continue
      if weight != font['weight']: continue
      style = font['style']
      break

  #————— weight if not present find font with same family & style, and steal weight

  if weight == '':
    for font in font_list:
      if family != font['family']: continue
      if style != font['style']: continue
      weight = font['weight']
      break

  #————— url

  for font in font_list:
    if family != font['family']: continue
    if weight!= font['weight']: continue
    if style != font['style']: continue
    url = font['url']
    break

  #————— done!

  chosen = {'family': family, 'style': style, 'weight': weight,  'url': url,} # eight, 600, normal
  

  return chosen
  
#———————————————————————————————————————— css_file_from_tag(pasted_link)

def css_file_from_tag(pasted_link):

  parts = pasted_link.split('"') # <link rel="stylesheet" href="https://use.typekit.net/jpl1zaz.css">
  stylesheet = file_from_url(parts[3])
  if stylesheet[0:2] != '/*': return ''
  return stylesheet


#:::::::::::::::::::::::::::::::::::::::: utility methods

#———————————————————————————————————————— simplified(str)
#
#   has been tested, and 8 returns eight
#
#   lower case, no dashes or spaces
#   to compare svg references to adobe css refs
#   beware of the font called '8'

def simplified(str):

  if is_valid_integer(str):
    str = convert_number_to_word(str)

  return str.replace(' ', '').replace('-', '').lower()

#———————————————————————————————————————— add_dashes(txt)
#
#   requires original case (won't work on all lower case input)
#
#   splits a name into parts separated by -, one character at a time
#   - ' ' —› '-' Open Sans —› Open-Sans
#   - xX —› x-X     OpenSans —› Open-Sans
#   - XXx —› X-Xx   IBMPlex —› IBM-Plex
#
#   split at each -

def add_dashes(txt):
  if txt == '' or len(txt) == 1: return txt

  result = ''

  for x in range(len(txt) - 1):

    if txt[x] == ' ':  # space
      result += '-'; continue

    if txt[x].islower() and txt[x+1].isupper(): # transition lower › upper
      result += txt[x] + '-'; continue

    if x > 0:
      if txt[x-1].isupper() and txt[x].isupper() and txt[x+1].islower(): # transition upper > lower
        result = result[0:len(result)-1] + txt[x-1] + '-' + txt[x]; continue

    result += txt[x]

  result += txt[x+1]

  return result

#———————————————————————————————————————— file_from_url(url)
#
#    given URL, returns contents or error

def file_from_url(url):
  try:
    response = requests.get(url, timeout=3)
    return response.text
  except Exception as e:
    return str(e)

#———————————————————————————————————————— is_valid_integer(s):

def is_valid_integer(s):
  try:
    int(s)
    return True
  except ValueError:
    return False

#———————————————————————————————————————— convert_number_to_word(family)
#
#   for font called '8'

word_equivalents = {
  '1'      : 'one',
  '2'      : 'two',
  '3'      : 'three',
  '4'      : 'four',
  '5'      : 'five',
  '6'      : 'six',
  '7'      : 'seven',
  '8'      : 'eight',
  '9'      : 'nine',
  '0'      : 'zero',
}

def convert_number_to_word(family):

  if not family.isdecimal(): return family
  if len(family) > 1: return family

  return word_equivalents[family]

#———————————————————————————————————————— fix_caps(entry)
#
#   exists to convert FuturaPT-ExtraBoldObl to FuturaPT-ExtraboldObl
#   later on in process the style will be found correctly
#
#   accepts a string and does a dict search/replace

caps_replacements = {
  'ExtraLight' : 'Extralight',
  'Extra-Light': 'Extralight',
  'ExtraBold'  : 'Extrabold',
  'Extra-Bold' : 'Extrabold',
  'SemiBold'   : 'Semibold',
  'Semi-Bold'  : 'Semibold',
  'UltraBlack' : 'Ultrablack',
  'Ultra-Black': 'Ultrablack',
}

def fix_caps(entry):
  if entry == '': return entry

  for key in caps_replacements:
    if entry.find(key) > 0:
      entry = entry.replace(key, caps_replacements[key])
      break

  return entry

#———————————————————————————————————————— matching_chars(str1, str2)
#
#   number of matching chars at beginning of name
#   + nmuber of matching chars at end of name

def matching_chars(str1, str2):

  len1 = len(str1)
  len2 = len(str2)

  counter = min(len1, len2)
  matching = 0

  for x in range(0, counter):
    if str1[x:x+1] == str2[x:x+1]:
      matching += 1
    else: break

  for x in range(0, counter):
    if str1[len1-x-1:len1-x] == str2[len2-x-1:len2-x]:
      matching += 1
    else: break

  return matching

# test
w1 = '300'
w2 = '300'
print( 'matching_chars: '+str(matching_chars(w1, w2)))


#:::::::::::::::::::::::::::::::::::::::: fin

#   acierbatgris:400:normal
#   acierbatnoir:400:normal
#   acierbatoutline:400:normal
#   acierbatsolid:400:normal
#   acierbatstrokes:400:normal
#   active:400:normal
#   altacalifornia:400:normal
#   asimovsans:400:normal
#   bdgeminis:400:normal
#   bdra3mik:400:normal
#   cooperblackstd:400:normal
#   eight:400:normal
#   fffolkrough:400:normal
#   fitcompressed:400:normal
#   fitextrawide:400:normal
#   fitskyline:400:normal
#   fitwide:400:normal
#   futurapt:300:italic
#   futurapt:300:normal
#   futurapt:400:italic
#   futurapt:400:normal
#   futurapt:500:italic
#   futurapt:500:normal
#   futurapt:600:italic
#   futurapt:600:normal
#   futurapt:700:italic
#   futurapt:700:normal
#   futurapt:800:italic
#   futurapt:800:normal
#   futuraptbold:700:italic
#   futuraptbold:700:normal
#   marshmallowfluff:400:normal
#   newsgothicstd:400:normal
#   nove:400:normal
#   proximanova:100:normal
#   proximanova:300:normal
#   proximanova:400:normal
#   proximanova:500:normal
#   proximanova:600:normal
#   proximanova:700:normal
#   proximanova:800:normal
#   proximanova:900:normal
#   sofachrome:100:normal

