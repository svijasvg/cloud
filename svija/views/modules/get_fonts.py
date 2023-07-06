
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

#———————————————————————————————————————— equivalences

# how do display fonts that don't really have a weight work?
# french roast: <link rel="stylesheet" href="https://use.typekit.net/ycw1wbc.css"> weight:400

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
  'default'    : '400',
}

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

style_equivalents = {
  'cond'      : 'condensed',
  'oblique'   : 'Italic',
  'obl'       : 'Italic',
  'italic'    : 'Italic',
}


#:::::::::::::::::::::::::::::::::::::::: main method

#———————————————————————————————————————— ▼ def get_fonts()

def get_fonts():
  all_fonts    = Font.objects.filter(enabled=True)
  woff_fonts   = Font.objects.filter(enabled=True).exclude(woff='')

  adobe_fonts      = Font.objects.filter(enabled=True).exclude(adobe_link='')
  new_adobe_fonts  = Font.objects.filter(Q(enabled=True) & Q(family='')).exclude(adobe_link='')

  google_fonts = Font.objects.filter(Q(enabled=True) & Q(google = True))
  new_google_fonts = Font.objects.filter(Q(enabled=True) & Q(google = True) & Q(family=''))

  empty_woff   = "@font-face {{ font-family:'{}'; src:{}'){}; }}"

  woff_css = adobe_css = google_css = ''
  adobe_fonts_array  = []
  google_fonts_array = []
  google_link  = ''


#:::::::::::::::::::::::::::::::::::::::: add new fonts

#———————————————————————————————————————— add new Adobe fonts

  for this_font in new_adobe_fonts:

    [family, style] = adobe_split(this_font.svg_ref)
    this_font.family = add_spaces(family)
    this_font.style  = style
    this_font.save()

#———————————————————————————————————————— add new Google fonts

  for this_font in new_google_fonts:

    [family, style] = google_split(this_font.svg_ref)
    this_font.family = add_spaces(family)
    this_font.style  = style
    this_font.save()


#:::::::::::::::::::::::::::::::::::::::: fonts are set up, now generate css

#———————————————————————————————————————— ▼ loop through fonts

  for this_font in all_fonts:

#———————————————————————————————————————— 1: web font (Arial etc.) WOFF filename contains ","
#
#   need to have several variations (as in a typical CSS declaration)

    woff = this_font.woff
    if woff != '':

      if woff.find(',') > 0: # local fonts
        # adds to css: src: local('Arial'), local('Arial MT'), local('Arial Regular'); }
        font_format = ''
        locals = woff.replace(', ',',').split(',')
        woff = "local('"+"'), local('".join(locals)
        woff_css += '\n'+ empty_woff.format(svg_ref, woff, font_format)
        continue

#———————————————————————————————————————— 2: WOFF filename

    # remove everything in beginning of path if necessary
    # /Users/Main/Library/Mobile Documents/com~apple~CloudDocs/Desktop/svija.dev/sync/SVIJA/Fonts/Woff Files/clarendon.woff
  

    woff = this_font.woff
    if woff != '':

      if woff.find('/') > -1:            # remove all but filename
        woff = woff.rpartition("/")[2]
        this_font.woff = woff
        this_font.save()

      if woff.find('woff2') > 0:
        font_format = " format('woff2')"
        woff_url = "url('/fonts/" + woff
        woff_css  += '\n'+ empty_woff.format(svg_ref, woff_url, font_format)
        continue

      else:
        font_format = " format('woff')"
        woff_url = "url('/fonts/" + woff
        woff_css += '\n'+ empty_woff.format(svg_ref, woff_url, font_format)
        continue

#———————————————————————————————————————— generate adobe css
#
#    separate from earlier loop because all adobe fonts are combined
#    into a single CSS block, with only one copyright comment section

  if len(adobe_fonts_array) > 0:

    # get comments from first font in list
    adobe_css = comments_only(adobe_fonts_array[0].adobe)
  
    for f in adobe_fonts_array:
      adobe_css += "\n@font-face { font-family:'"+f.svg_ref + "'; src:url("+f.adobe_url+") format('woff'); }"

#———————————————————————————————————————— generate google fonts link

  if len(google_fonts_array) > 0:
    link_str = '  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family={}">'
    google_link = link_str.format(('|').join(google_fonts_array))

#———————————————————————————————————————— ▲ return link & css

  return google_link, woff_css + adobe_css


#:::::::::::::::::::::::::::::::::::::::: main methods

#———————————————————————————————————————— adobe_split(svg_ref)
#
#   if it's adobe, we search for one of the weights and
#   split on it, then use family + weight + rest (style),
#   with slashes changed to single spaces
#   style is optional

# results = ''
# for key in adobe_weights:
#   if txt.find(key) > 0:
#     txt = txt.replace(key, adobe_weights[key])

def adobe_split(svg_ref):
  family = weight = style = ''
  svg_low = svg_ref.lower()

  for key in adobe_weights:
    if svg_low.find(key) > 0:
      parts = svg_low.split(key)

      family = svg_ref[:len(parts[0])]
      weight = adobe_weights[key]

      if parts[1] != '':
        style = svg_ref[0 - len(parts[1]):]

      break

# return [family, 'xxx'] # 8-

  if family == '':                      # nothing was found
    family = svg_ref

  if family[-1:] == '-':                # remove trailing slashes
    family = family[:-1]                # works

# return [family, 'xxx'] # 8 

# possibly convert family FuturaPT to Futura PT 

  if style != '':
    style_low = style.lower()
  
    if style_low in style_equivalents:
      style = style_equivalents[style_low]
    else:
      # throw it all away, we don't know
      family = svg_ref
      weight = ''
      style  = ''

  if family != '':                      # changes - to space for legibility
    family = family.replace('-', ' ')   # might cause problems

  if weight == '':
    weight = adobe_weights['default']

  return [family, weight + style]

#———————————————————————————————————————— google_split(svg_ref)
#
#   if it's google, we search for one of the weights and
#   split on it, then use family + weight + rest (style),
#   with slashes changed to single spaces
#   style is optional

def google_split(svg_ref):
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

# return [family, weight+':'+style] # 8-

  if family == '':                      # nothing was found
    family = svg_ref

  if family[-1:] == '-':                # remove trailing slashes
    family = family[:-1]                # works

# return [family, 'xxx'] # 8 

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
      family = svg_ref[:len(style) + 1]

  if family != '':                      # changes - to space for legibility
    family = family.replace('-', ' ')   # might cause problems

  return [family, weight + style]


#:::::::::::::::::::::::::::::::::::::::: adobe font methods

#———————————————————————————————————————— get_adobe_font(this_font)
#
#    user pastes a string like
#   
#    <link rel="stylesheet" href="https://use.typekit.net/jpl1zaz.css">
#
#    returns css, name, woff url, style and weight

def get_adobe_font(font):

  if font.adobe_link[0] != '<': return font.adobe

  #—————————————————————————————————————— get url then CSS file

  bits = font.adobe_link.split('"') # <link rel="stylesheet" href="https://use.typekit.net/jpl1zaz.css">

  if len(bits) < 4:
    return '', '', '⚠️ check pasted link', '', ''

  file_contents = file_from_url(bits[3])

  if file_contents[0:2] != '/*':
    return '', '', '⚠️ check pasted link', '', ''

  #—————————————————————————————————————— find match for font

  css_fonts = font_list_from_css(file_contents)

  best_value  = 0
  best_choice = 0

  target_font = add_spaces(font.svg_ref) # returns acier-bat-text-gris
  target_font = weights_to_numbers_adobe(target_font)
  target_font = clean_styles(target_font)

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

# file_contents    = '/*    '+font.adobe + '    */\n' + file_contents
  final_font = css_fonts[best_choice]

  return file_contents, final_font['name'], final_font['woff'], final_font['style'], final_font['weight']

#———————————————————————————————————————— font_list_from_css(this_font)
#
#   returns list of fonts found in css
#
#   returned fonts are arrays:
#   - name: family name
#   - woff: woff source URL
#   - style
#   - weight (converted to number)
#
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

def font_list_from_css(css_src):

#———————————————————————————————————————— initialise

  font_list = []
  start_index = 0

  how_many = int(css_src.count('font-face')) # because each font is listed once with source, then once with class

  for x in range(how_many):

#   - name1, name2:     start & end indexes
#   - woff1, woff2:     start & end indexes
#   - style1, style2:   start & end indexes
#   - weight1, weight2: start & end indexes

    #———————————————————————————————————— get family indexes
  
    this_adobe  = {}
  
    name_first = css_src.find('font-family', start_index) + 13
    name_last  = css_src.find('"', name_first)
  
    this_adobe['name1'] = name_first
    this_adobe['name2'] = name_last
    this_adobe['name']  = css_src[name_first:name_last]
  
    #———————————————————————————————————— get woff indexes CAN SIMPLIFY — SEE BELOW

#   NOTE: the three links are all the same except for the character before the ?:
#   
#   L = woff2
#   d = woff
#   a = opentype
#   I can use this fact to simplify the code.
  
    woff2      = css_src.find('url("', name_last) + 5
    woff_first = css_src.find('url("', woff2) + 5
    woff_last  = css_src.find('")', woff_first)
  
    this_adobe['woff']  = css_src[woff_first:woff_last]
  
    #———————————————————————————————————— get style indexes
  
    style_first = css_src.find('font-style:', name_last) + 11
    style_last  = css_src.find(';', style_first)
  
    this_adobe['style']  = css_src[style_first:style_last]
  
    #———————————————————————————————————— get weight indexes
  
    weight_first = css_src.find('font-weight:', name_last) + 12
    weight_last  = css_src.find(';', weight_first)
  
    this_adobe['weight']  = css_src[weight_first:weight_last]
  
    #———————————————————————————————————— add font to list

    font_list.append(this_adobe)
    start_index = style_last


  return font_list

#———————————————————————————————————————— clean_styles(txt)

#   accepts a string like FuturaPT-Bold-Obl, and replaces
#   obl by italic, thin by 100 etc.

def clean_styles(txt):

  results = ''
  for key in style_equivalents:
    if txt.find(key) > 0:
      txt = txt.replace(key, style_equivalents[key])

  return txt

#———————————————————————————————————————— italics_present(txt1, txt2)

def italics_present(targ, cand):

  if cand.find('italic') > 0:
     if targ.find('italic') < 1:
       return -1

  return 0


#:::::::::::::::::::::::::::::::::::::::: utility methods

#———————————————————————————————————————— add_spaces(txt)
#
#   splits a name into parts separated by -
#   - if this char is dash, replace with space
#   - if this char is lower & next is upper, add space between them
#   - if this car is upper & prev is upper & next is lower, add space after this char
#
#   split at each -

def add_spaces(txt):
  
  result = ''

  for x in range(len(txt) - 1):

    if txt[x] == ' ':  # space
      result += ' '
      continue

    if txt[x].islower() and txt[x+1].isupper(): # transition lower › upper
      result += txt[x] + ' '
      continue

    if x > 0:
      if txt[x-1].isupper() and txt[x].isupper() and txt[x+1].islower(): # transition upper > lower
        result = result[0:len(result)-1] + txt[x-1] + ' ' + txt[x]
        continue

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

#———————————————————————————————————————— comments_only(css)

def comments_only(css):
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


#:::::::::::::::::::::::::::::::::::::::: fin
