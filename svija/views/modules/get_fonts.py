
#:::::::::::::::::::::::::::::::::::::::: get_fonts.py

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

#———————————————————————————————————————— style equivalens

# how do display fonts that don't really have a weight work?
# french roast: <link rel="stylesheet" href="https://use.typekit.net/ycw1wbc.css"> weight:400

style_equivalents = {
  'cond'      : 'condensed',
  'oblique'   : 'Italic',
  'obl'       : 'Italic',
  'italic'    : 'Italic',
}


#:::::::::::::::::::::::::::::::::::::::: main method

#———————————————————————————————————————— ▼ def get_fonts()

def get_fonts():
  enabled_fonts    = Font.objects.filter(enabled=True)
  woff_fonts   = Font.objects.filter(enabled=True).exclude(woff='')

  adobe_fonts      = Font.objects.filter(enabled=True).exclude(adobe_pasted='')
  new_adobe_fonts  = Font.objects.filter(Q(enabled=True) & Q(adobe_sheet='')).exclude(adobe_pasted='')

  google_fonts = Font.objects.filter(Q(enabled=True) & Q(google = True))
  new_google_fonts = Font.objects.filter(Q(enabled=True) & Q(google = True) & Q(family=''))

  adobe_fonts_array  = []
  google_fonts_array = []
  google_link  = ''


#:::::::::::::::::::::::::::::::::::::::: add new fonts

#———————————————————————————————————————— add new WOFF fonts

  for this_font in woff_fonts:

    # remove everything in beginning of path if necessary
    # /Users/Main/Library/Mobile Documents/com~apple~CloudDocs/Desktop/svija.dev/sync/SVIJA/Fonts/Woff Files/clarendon.woff

    woff = this_font.woff
    if woff.find('/') > -1:            # remove all but filename
      woff = woff.rpartition("/")[2]
      this_font.woff = woff
      this_font.save()

#———————————————————————————————————————— add new Adobe fonts

#   right now, the Adobe stylesheet is parsed again for each new font
#   but generally, there will only be one stylesheet for a site
# 
#   so I could keep the contents and reuse it for each font
#   but I need a way to track which sheets were integrated
#   so that if someone uses two different adobe sheets
#   it will still work

#   <link rel="stylesheet" href="https://use.typekit.net/ycw1wbc.css">

  for this_font in new_adobe_fonts:

    # check for valid link
    if this_font.adobe_pasted[0] != '<':   # contents is not "<link rel..."
      this_font.adobe_url = "⚠️ Error in pasted link"
      this_font.adobe_sheet = ''
      this_font.save()
      continue

    # get list of fonts in stylesheet
    font_list, stylesheet = font_list_from_link(this_font.adobe_pasted)

    if type(font_list) is str:
      this_font.adobe_url = font_list
      this_font.adobe_sheet = ''
      this_font.save()
      continue

    # convert svg ref to [family, weight and style]
    target_font = interpret_adobe(this_font.svg_ref)

    # find match between target_font and font_list
    font = best_adobe_match(target_font, font_list)

    # if match failed
    if type(font) is str:
      this_font.adobe_url = font
      this_font.adobe_sheet = stylesheet
      this_font.save()
      continue

    # all is good so save info
    this_font.family      = font['family']
    this_font.weight      = font['weight']
    this_font.style       = font['style']
    this_font.adobe_url   = font['url']
    this_font.adobe_sheet = stylesheet
    this_font.save()


#———————————————————————————————————————— add new Google fonts

  for this_font in new_google_fonts:

    [family, style] = interpret_google(this_font.svg_ref)
    this_font.family = add_dashes(family)
    this_font.style  = style
    this_font.save()


#:::::::::::::::::::::::::::::::::::::::: fonts are set up, now generate css

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
      adobe_css += "\n@font-face { font-family:'"+this_font.svg_ref + "'; src:url("+this_font.adobe_url+") format('woff'); }"

#———————————————————————————————————————— generate google fonts link

  google_css = ''
  if len(google_fonts_array) > 0:
    link_str = '  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family={}">'
    google_link = link_str.format(('|').join(google_fonts_array))

#———————————————————————————————————————— ▲ return link & css

  return google_link, woff_css + adobe_css


#:::::::::::::::::::::::::::::::::::::::: google-related methods

#———————————————————————————————————————— interpret_google(svg_ref)
#
#   if it's google, we search for one of the weights and
#   split on it, then use family + weight + rest (style),
#   with slashes changed to single spaces
#   style is optional

google_weights = {
  'extralight':'200',
  'semibold'  :'600',
  'extrabold' :'800',
  'thin'      :'100',
  'light'     :'300',
  'regular'   :'400',
  'medium'    :'500',
  'bold'      :'700',
  'black'     :'900',
  'default'   :'400',
}

def interpret_google(svg_ref):

  family = weight = style = ''
  svg_low = svg_ref.lower()

  for key in google_weights:
    if svg_low.find(key) > 0:
      parts = svg_low.split(key)

      family = svg_ref[:len(parts[0])]
      weight = google_weights[key]

#     return [family, key] # OpenSans, light
      if parts[1] != '':
        style = svg_ref[0 - len(parts[1]):]

      break

  if family == '':                      # nothing was found
    family = svg_ref

# possibly convert family FuturaPT to Futura PT 

  style = style.replace('-', '')

  if style != '':
    style_low = style.lower()
  
    if style_low in style_equivalents:
      style = style_equivalents[style_low]
    else:
      # throw it all away, we don't know
      family = svg_ref
      weight = ''
      style  = ''

  if weight == '': # Poppins-Italic
    weight = google_weights['default']
    parts = svg_ref.split('-')
    last = parts[len(parts) - 1].lower()

    if last in style_equivalents:
      style = style_equivalents[last]
      family = svg_ref[:len(svg_ref) - len(style)]

  if family[-1:] == '-':                # remove trailing dashes
    family = family[:-1]                # works

  if family != '':                      # changes - to space for legibility
    family = family.replace('-', ' ')   # might cause problems

  return [family, weight + style]


#:::::::::::::::::::::::::::::::::::::::: adobe-related methods

#———————————————————————————————————————— interpret_adobe(svg_ref)
#
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

adobe_weights = {
  'extralight' : '200',
  'extra-light': '200',
  'extrabold'  : '800',
  'extra-bold' : '800',
  'demi'       : '600',
  'semibold'   : '600',
  'semi-bold'  : '600',
  'ultrablack' : '900',
  'ultra-black': '900',
  'thin'       : '100',
  'light'      : '300',
  'book'       : '400',
  'regular'    : '400',
  'heavy'      : '600',
  'medium'     : '500',
  'bold'       : '700',
  'black'      : '800',
  'default'    : '',
}
adobe_styles = {
  'cond'      : 'condensed',
  'oblique'   : 'italic',
  'obl'       : 'italic',
  'italic'    : 'italic',
  'default'   : 'normal',
}

def interpret_adobe(svg_ref):

  # need to replace ExtraBlack with Extrablack, it will work out well
  svg_ref = fix_caps_adobe(svg_ref)

  raw_string = add_dashes(svg_ref).lower()

  parts = raw_string.split('-')

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

#———————————————————————————————————————— parse_adobe_sheet(font)

def parse_adobe_sheet(font):

  #—————————————————————————————————————— validate argument

  if font.adobe_pasted[0] != '<': return font.adobe

  #—————————————————————————————————————— get url then CSS file

  parts = font.adobe_pasted.split('"') # <link rel="stylesheet" href="https://use.typekit.net/jpl1zaz.css">

  stylesheet = file_from_url(parts[3])

  if stylesheet[0:2] != '/*': return '', '', '⚠️ check pasted link', '', ''

  #—————————————————————————————————————— find match for font

  css_fonts = font_list_from_link(stylesheet)

  best_value  = 0
  best_choice = 0

  target_font = add_dashes(font.svg_ref) # returns acier-bat-text-gris
  target_font = weights_to_numbers_adobe(target_font)
  target_font = replace_styles(target_font)

  indx        = 0

  for this_font in css_fonts:

    candidate  = (this_font['name'] + '-' + this_font['style'] + '-' + this_font['weight']).lower()

    v  = match_count(target_font, candidate)
    v += italics_present(target_font, candidate) # remove a point if only candidate has italic

    if v > best_value:
      best_choice = indx
      best_value  = v

    indx += 1

  #———————————————————————————————————————— return best match

# file_contents    = '/*    '+font.adobe_sheet + '    */\n' + file_contents
  final_font = css_fonts[best_choice]

  return file_contents, final_font['name'], final_font['woff'], final_font['style'], final_font['weight']


#———————————————————————————————————————— font_list_from_link(this_font)
#
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

#———————————————————————————————————————— best_adobe_match(target_font, font_list) NOT FINISHED
#
#   accepts:
#
#   target_font {family, weight, style}
#   font_list  [{'family': family,  'url': url, 'style': style, 'weight': weight,} ... ]
#   

def best_adobe_match(target_font, font_list):

  family = style = weight = url = ''

  #————— get best family match (breaks for family futura-pt-bold)

  counter   = 0
  max       = 0
  max_which = 0

  for font in font_list:

    # match at beginning of family name + match at end of family name
    this_max = char_match(target_font['family'], font['family'])
    if this_max > max:
      max = this_max
      max_which = counter

    counter += 1

  #————— family is established
  
  if max == 0:
    return '⚠️ Font not found in stylesheet'

  else:
    family = font_list[max_which]['family']

  #————— get best style match

  counter   = 0
  max       = 0
  max_which = 0

  for font in font_list:
    if family != font['family']: continue

    this_max = char_match(target_font['style'], font['style'])
    if this_max > max:
      max = this_max
      max_which = counter

    counter += 1

  #————— style established
  
  if max == 0:
    style = ''
  else:
    style = font_list[max_which]['style']

  #————— get best weight match

  counter   = 0
  max       = 0
  max_which = 0

  for font in font_list:
    if family != font['family']: continue

    this_max = char_match(target_font['weight'], font['weight'])
    if this_max > max:
      max = this_max
      max_which = counter

    counter += 1

  #————— weight established
  
  if max == 0:
    weight = ''
  else:
    weight = font_list[max_which]['weight']

  #————— get url

  probable_weight = ''

  for font in font_list:
    if family == font['family']:
       if style == font['style']:
         if weight == font['weight']:
           url = font['url']
           break
         else:
           url = font['url']
           probable_weight = font['weight']

  if weight == '': weight = probable_weight

  chosen = {'family': family, 'style': style, 'weight': weight,  'url': url,}
  
  return chosen

# target_font['url'] = 'this is the url'
  
#———————————————————————————————————————— char_match(str1, str2)
#
#   number of matching chars at beginning of name
#   + nmuber of matching chars at end of name

def char_match(str1, str2):

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


#:::::::::::::::::::::::::::::::::::::::: utility methods

#———————————————————————————————————————— replace_styles(txt)

#   accepts a string like FuturaPT-Bold-Obl, and replaces
#   obl by italic, thin by 100 etc.

def replace_styles(txt):

  results = ''
  for key in style_equivalents:
    if txt.find(key) > 0:
      txt = txt.replace(key, style_equivalents[key])

  return txt

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

#———————————————————————————————————————— weights_to_numbers_adobe(txt)

#   accepts a string like FuturaPT-Bold-Obl, and replaces
#   obl by italic, thin by 100 etc.

# receives futura-pt-condensed-extra-bold-italic

def weights_to_numbers_adobe(txt):

  results = ''
  for key in adobe_weights:
    if txt.find(key) > 0:
      txt = txt.replace(key, adobe_weights[key])

  return txt

#———————————————————————————————————————— first_comment(css)

def first_comment(css):
  start = css.find('/*\n')
  end   = css.find('"}*/\n') + 4
  return css[start:end] + '\n'

#———————————————————————————————————————— match_count(arr1, arr2)
#
#    returns number of matches in two strings
#
#    each string is hyphen-separated list of words

def match_count(str1, str2):

  arr1 = str1.lower().split('-')
  arr2 = str2.lower().split('-')

  len_1 = len(arr1)
  len_2 = len(arr2)

  if len_1 > len_2:
    first  = arr1
    second = arr2
  else:
    first  = arr2
    second = arr1

  matches = 0

  for element1 in first:
    for element2 in second:
      if element1 == element2:
        matches += 1
  
  return matches

#———————————————————————————————————————— italics_present(txt1, txt2)

def italics_present(targ, cand):

  if cand.find('italic') > 0:
     if targ.find('italic') < 1:
       return -1

  return 0

#———————————————————————————————————————— convert_number_to_word(family)

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

#———————————————————————————————————————— fix_caps_adobe(entry)
#
#   exists to convert FuturaPT-ExtraBoldObl to FuturaPT-ExtraboldObl
#   later on in process the style will be found correctly
#
#   accepts a string and does a dict search/replace

adobe_replacements = {
  'ExtraLight' : 'Extralight',
  'Extra-Light': 'Extralight',
  'ExtraBold'  : 'Extrabold',
  'Extra-Bold' : 'Extrabold',
  'SemiBold'   : 'Semibold',
  'Semi-Bold'  : 'Semibold',
  'UltraBlack' : 'Ultrablack',
  'Ultra-Black': 'Ultrablack',
}

def fix_caps_adobe(entry):
  if entry == '': return entry

  for key in adobe_replacements:
    if entry.find(key) > 0:
      entry = entry.replace(key, adobe_replacements[key])
      break

  return entry


#:::::::::::::::::::::::::::::::::::::::: fin

