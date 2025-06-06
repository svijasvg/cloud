
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
from django.shortcuts import get_object_or_404
from svija.models import Font, Settings
import requests


#:::::::::::::::::::::::::::::::::::::::: main definition

def integrate_fonts():

#———————————————————————————————————————— remove conflicts
#
#   if google is checked, can't add adobe or woff
#   if woff is filled out, can't add adobe
#
#   adobe > google > woff

  all_fonts = Font.objects.filter(enabled=True)

  for this_font in all_fonts:

    if this_font.adobe:
      this_font.google = False
      this_font.woff   = ''
      this_font.save()
      
    if this_font.google:
      this_font.woff = ''
      this_font.save()

#———————————————————————————————————————— initialize new font arrays

#   I don't want to mess with information that may have been manualy modified


  new_adobe_fonts  = Font.objects.filter(Q(enabled=True) & Q(adobe=True) & Q(adobe_url=''))
  new_woff_fonts   = Font.objects.filter(enabled=True).exclude(woff='')

  new_google_fonts = Font.objects.filter(
                      ( Q(enabled = True ) & Q(google = True)               ) &
                      ( Q(family  = ''   ) | Q(weight = ''  ) | Q(style='') )
                     )


#———————————————————————————————————————— adobe fonts

#———————————————————————————————————————— initialization

#   in site settings:
#
#   <link rel="stylesheet" href="https://use.typekit.net/jpl1zaz.css">
#
#   there will only be a few different CSS sheets for Adobe Fonts —
#   normally, there will only be one.
#   
#   So I'm better off flooping through the fonts, and getting the
#   corret stylesheet into a dict, with the Adobe ID as the index
#   and a list of associated fonts & URLS
#   
#   otherwise I'm duplicationg work for each font that doesn't have to be done
#
#   in admin.py:
#   return obj.adobe_pasted[53:60]
#
#   <link rel="stylesheet" href="https://use.typekit.net/jpl1zaz.css">      svija.dev
#   <link rel="stylesheet" href="https://use.typekit.net/aav4onz.css">  alt.svija.dev (1 font)

  adobe_sheet     = ''
  adobe_font_list = []

  settings = get_object_or_404(Settings,enabled=True)
  adobe_project = settings.adobe_project

#———————————————————————————————————————— "while True" enables "break" to skip following code

  while True:

#———————————————————————————————————————— if user posted Adobe link, extract adobe ID

    if len(adobe_project) == 66:
      adobe_project = adobe_project[53:60]
      settings.adobe_project = adobe_project
      settings.save()

#———————————————————————————————————————— break: no new adobe fonts to treat

    if len(new_adobe_fonts) == 0: break

#———————————————————————————————————————— break: no adobe project ID

    if adobe_project == '':
      settings.adobe_sheet = _('enter adobe project id')
      settings.save()
      break 

#———————————————————————————————————————— break: Adobe ID is wrong length # 

    if len(adobe_project) != 7 and len(adobe_project) != 66:
      settings.adobe_sheet = _('adobe project wrong length')
      settings.save()
      break 
  
#———————————————————————————————————————— get adobe css file

    adobe_sheet_url = "https://use.typekit.net/" + adobe_project + ".css"
    adobe_sheet     = file_from_url(adobe_sheet_url)
  
#———————————————————————————————————————— break: css file is empty

    if adobe_sheet == '':
      settings.adobe_sheet = adobe_sheet_url + _('returned empty file')
      settings.save()
      break

#———————————————————————————————————————— get font list from css sheet

    adobe_font_list = fonts_from_adobe_sheet(adobe_sheet)
  
#———————————————————————————————————————— break: no fonts in css sheet

    if len(adobe_font_list) == 0:
      settings.adobe_sheet = adobe_sheet_url + _('contained no fonts')
      settings.save()
      break

#———————————————————————————————————————— save Adobe sheet

    settings.adobe_sheet = adobe_sheet
    settings.save()

#———————————————————————————————————————— ▼▲ get font url for each Adobe font

    for this_font in new_adobe_fonts:
  
      this_font = adobe_font_from_list(this_font, adobe_font_list) 

      if this_font == None: continue
  
      if this_font.adobe_url == '':
        this_font.adobe_url   = _('search css manually')
  
      this_font.save()

#———————————————————————————————————————— end "while True"

    break


#———————————————————————————————————————— woff & google fonts

#———————————————————————————————————————— add new WOFF fonts
#
#   this just means cleaning up path if someone
#   dragged it from the finder

  for this_font in new_woff_fonts:

#   # remove everything in beginning of path if necessary
#   # /Users/Main/Library/Mobile Documents/com~apple~CloudDocs/Desktop/svija.dev/SYNC/SVIJA/Fonts/Woff Files/clarendon.woff

    woff = this_font.woff
    if woff.find('/') > -1:
      woff = woff.rpartition("/")[2]
      this_font.woff = woff
      this_font.save()

#———————————————————————————————————————— COMMENTED add new Google fonts

#   this is seemingly unnecessary — all the necessary information is already
#   supplied via the SVG code

#   https://tech.svija.com/reference/fonts/google-fonts

# for this_font in new_google_fonts:

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

#———————————————————————————————————————— translation tables

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


#:::::::::::::::::::::::::::::::::::::::: main adobe method

#———————————————————————————————————————— adobe_font_from_list(this_font, candidates) 

def adobe_font_from_list(this_font, font_list):

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

        return this_font

#———————————————————————————————————————— weight & style match • test family matches candidate family

  for x in range(len(font_list)):
    candidate = font_list[x]

    if test_weight == candidate['weight'] and test_style == candidate['style']:

      if test_family == candidate['family']: #################################
        if this_font.weight == '': this_font.weight = test_weight
        if this_font.style  == '': this_font.style  = test_style
        this_font.adobe_url = candidate['url']

        return this_font

#———————————————————————————————————————— style matches • svg_ref matchs candidate family

  for x in range(len(font_list)):
    candidate = font_list[x]
    if test_style == candidate['style']:

      if test_svg_ref == candidate['family']: #################################
        if this_font.weight == '': this_font.weight = test_weight
        if this_font.style  == '': this_font.style  = test_style
        this_font.adobe_url = candidate['url']

        return this_font

#———————————————————————————————————————— weight matches • svg ref matches candidate family

  for x in range(len(font_list)):
    candidate = font_list[x]
    if test_weight == candidate['weight']:

      if test_svg_ref == candidate['family']:
        if this_font.weight == '': this_font.weight = test_weight
        if this_font.style  == '': this_font.style  = test_style
        this_font.adobe_url = candidate['url']

        return this_font

#———————————————————————————————————————— weight matches • test family matchs candidate family

  for x in range(len(font_list)):
    candidate = font_list[x]
    if test_weight == candidate['weight']:

      if test_family == candidate['family']:
        if this_font.weight == '': this_font.weight = test_weight
        if this_font.style  == '': this_font.style  = test_style
        this_font.adobe_url = candidate['url']

        return this_font

#———————————————————————————————————————— style matches • test family matchs candidate family

  for x in range(len(font_list)):
    candidate = font_list[x]
   
    if test_style == candidate['style']:

      if test_family == candidate['family']:
        if this_font.weight == '': this_font.weight = test_weight
        if this_font.style  == '': this_font.style  = test_style
        this_font.adobe_url = candidate['url']

        return this_font

#———————————————————————————————————————— svg ref matches candidate family

  for x in range(len(font_list)):
    candidate = font_list[x]
    if test_svg_ref == candidate['family']: ####################################
      if this_font.weight == '': this_font.weight = test_weight
      if this_font.style  == '': this_font.style  = test_style
      this_font.adobe_url = candidate['url']

      return this_font

#———————————————————————————————————————— test family matches candidate family

  for x in range(len(font_list)):
    candidate = font_list[x]
    if test_family == candidate['family']: ####################################
      if this_font.weight == '': this_font.weight = test_weight
      if this_font.style  == '': this_font.style  = test_style
      this_font.adobe_url = candidate['url']

      return this_font

#———————————————————————————————————————— difficult cases

# broken fonts: folk rough ot, aciet bat families

  best_match = 0
  final_font     = font_list[0]

  for x in range(len(font_list)):

    candidate  = font_list[x]
    this_match = count_overlap(test_svg_ref, candidate['family']+candidate['style'])

    if this_match > best_match:
      final_font = candidate
      best_match = this_match

  this_font.adobe_url   = final_font['url']

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

#:::::::::::::::::::::::::::::::::::::::: adobe-related secondary methods

#———————————————————————————————————————— translation tables

adobe_styles = {
  'oblique'   : 'italic',
  'obl'       : 'italic',
  'italic'    : 'italic',
  'book'      : 'normal',
}

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

#———————————————————————————————————————— contiguous_matching_chars(str1, str2) LOGIC PROBLEM

def contiguous_matching_chars(str1, str2):

  contiguous = 0
  max        = 0

  for x in range(len(str1)):

    if str1[x:x+1] == str2[x:x+1]:
      contiguous += 1
      if max < contiguous: max = contiguous

    else:
      contiguous = 0

  return max

#———————————————————————————————————————— count_overlap(str1, str2)

#   slides two strings across each other and counts the
#   number of matched strings of three or more characters

#   "    longerstringxxx    "
#   "shrtstr"

#   we want to match 3 or more, so we add len(shrtstr)-3 spaces to either end of longerstringxxx
#   then loop through len(shtrttr) sections on longerstring, removing one character at a time
#   each time count contiguous matches (separate function)

#   how many loops do we need? 

def count_overlap(str1, str2):

  minimum_matches = 3
  spaces          = '                                                                                                    '

  if len(str1) > len(str2):
    long_str = str1
    short_str = str2
  else:
    long_str = str2
    short_str = str1

  if len(short_str) > minimum_matches:
    spaces = spaces[0:len(short_str)-minimum_matches]
  
  long_str = spaces + long_str + spaces

  # slide the strings

  total_matches = 0

  for x in range(len(long_str) - len(short_str)):
  
    comparison_str = long_str[x:len(short_str)+x]
    matches = contiguous_matching_chars(short_str, comparison_str)
    if matches > minimum_matches:
      total_matches += matches

  return total_matches

#———————————————————————————————————————— fonts_from_adobe_sheet(css_str)
#
#   extracts fonts from and Adobe typekit CSS sheet
#
#   https://use.typekit.net/jpl1zaz.css?lkjsdlmkqsd
#
#   returns a list of font dictionaries with
#   family, weight, style and woff2 src URL

def fonts_from_adobe_sheet(css_str):
  if css_str == '': return []
  if '@font-face' not in css_str: return []

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

#———————————————————————————————————————— derive_adobe_style(font)

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

