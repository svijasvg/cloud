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

#———————————————————————————————————————— equivalences

# how do display fonts that don't really have a weight work?
# french roast: <link rel="stylesheet" href="https://use.typekit.net/ycw1wbc.css"> weight:400

adobeWeights = {
  'extralight':'200',
  'semibold'  :'600',
  'ultrablack':'900',
  'thin'      :'100',
  'light'     :'300',
  'regular'   :'400',
  'medium'    :'500',
  'bold'      :'700',
  'black'     :'800',
}

googleWeights = {
  'extralight':'200',
  'semibold'  :'600',
  'extrabold' :'800',
  'thin'      :'100',
  'light'     :'300',
  'regular'   :'400',
  'medium'    :'500',
  'bold'      :'700',
  'black'     :'900',
}


#:::::::::::::::::::::::::::::::::::::::: main method

#———————————————————————————————————————— ▼ get_fonts()

def get_fonts():
  font_objs    = Font.objects.all()
  css_str      = "@font-face {{ font-family:'{}'; src:{}'){}; }}"
  woff_css     = ''
  adobe_css    = ''
  adobe_fonts  = []
  google_fonts = []
  google_link  = ''

#———————————————————————————————————————— ▼ loop through all fonts

  for this_font in font_objs:
    if not this_font.enabled: continue

#———————————————————————————————————————— original CSS reference

    svg  = this_font.svg_ref
    woff = this_font.woff

#———————————————————————————————————————— web fonts (Arial etc.) contains ,
#
#   need to have several variations (as in a typical CSS declaration)

    if woff != '':

      if woff.find(',') > 0: # local fonts
        # adds to css: src: local('Arial'), local('Arial MT'), local('Arial Regular'); }
        font_format = ''
        locals = woff.replace(', ',',').split(',')
        woff = "local('"+"'), local('".join(locals)
        woff_css += '\n'+ css_str.format(svg, woff, font_format)
        continue

#———————————————————————————————————————— woff fonts (macOS)

    # remove everything in beginning of path if necessary
    # /Users/Main/Library/Mobile Documents/com~apple~CloudDocs/Desktop/svija.dev/sync/SVIJA/Fonts/Woff Files/clarendon.woff
  

    if woff != '':

      if woff.find('/') > -1:            # remove all but filename
        woff = woff.rpartition("/")[2]
        this_font.woff = woff
        this_font.save()

      if woff.find('woff2') > 0:
        font_format = " format('woff2')"
        woff = "url('/fonts/" + woff
        woff_css  += '\n'+ css_str.format(svg, woff, font_format)
        continue

      font_format = " format('woff')"
      woff = "url('/fonts/" + woff
      woff_css += '\n'+ css_str.format(svg, woff, font_format)
      continue

#———————————————————————————————————————— adobe fonts

#   comments
#
#   adobe_link = pasted by user from Adobe site
#   adobe_url  = woff file URL found in below
#   adobe      = contents of CSS file found at adobe_link
#
#   4 cases:
#   
#   - no pasted link: skip it all
#   - pasted link, but erroneous
#   - pasted link, url is already filled
#   - pasted link, url is not filled
      
    if this_font.adobe_link != '':

      if this_font.adobe_url != '':
        if this_font.adobe_url[0] == 'h':   # url is already found
          adobe_fonts.append(this_font)
          continue

      if this_font.adobe_link[0] != '<':   # contents is not <link rel="stylesheet" href="https://use.typekit.net/jpl1zaz.css">
        this_font.adobe_url = "⚠️ Error in pasted link"
        this_font.adobe = ''
        this_font.save()
        continue

      # extract URL from retrieved CSS

      a_css, a_name, a_url, a_style, a_weight = get_adobe_font(this_font)

      this_font.family    = a_name
      this_font.adobe     = a_css
      this_font.adobe_url = a_url
      this_font.style     = a_weight +' '+a_style

      this_font.save()

      if (a_url[0] == 'h'):
        adobe_fonts.append(this_font)

      continue
        
#———————————————————————————————————————— ▲ google fonts /end loop

# for google fonts CSS, we need family=Open+Sans:300|Open+Sans:300italic|Open+Sans:600
# no spaces between weight & style

    if this_font.google:
      style = this_font.style

      for word, number in googleWeights.items():
        style = style.lower().replace(word, number)

      style = style.replace(' ','')
      famly = this_font.family.replace(' ','+')
      google_fonts.append(famly+':'+style)

#———————————————————————————————————————— generate adobe css
#
#    separate from earlier loop because all adobe fonts are combined
#    into a single CSS block, with only one copyright comment section



  if len(adobe_fonts) > 0:

    # get comments from first font in list
    adobe_css = comments_only(adobe_fonts[0].adobe)
  
    for f in adobe_fonts:
      adobe_css += "\n@font-face { font-family:'"+f.svg_ref + "'; src:url("+f.adobe_url+") format('woff'); }"

#———————————————————————————————————————— generate google fonts link

  if len(google_fonts) > 0:
    link_str = '  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family={}">'
    google_link = link_str.format(('|').join(google_fonts))

#———————————————————————————————————————— ▲ return link & css

  return google_link, woff_css + adobe_css


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

  target_font = add_dashes(font.svg_ref) # returns acier-bat-text-gris
  target_font = weights_to_numbers(target_font)
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

style_equivalents = {
  'cond-'       : 'condensed-',
  'oblique'     : 'italic',
  'obl'         : 'italic',
}

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

#———————————————————————————————————————— add_dashes(txt)
#
#   splits a name into parts separated by -
#   - if this char is space, replace with -
#   - if this char is lower & next is upper, add - between them
#   - if this car is upper & prev is upper & next is lower, add - after this char
#
#   split at each -

def add_dashes(txt):
  
  dashes = ''

  for x in range(len(txt) - 1):


    if txt[x] == ' ':  # space
      dashes += '-'
      continue

    if txt[x].islower() and txt[x+1].isupper(): # transition lower › upper
      dashes += txt[x] + '-'
      continue

    if x > 0:
      if txt[x-1].isupper() and txt[x].isupper() and txt[x+1].islower(): # transition upper > lower
        dashes = dashes[0:len(dashes)-1] + txt[x-1] + '-' + txt[x]
        continue

    dashes += txt[x]

  dashes += txt[x+1]
  dashes = dashes.lower()

  return dashes

#———————————————————————————————————————— file_from_url(url)
#
#    given URL, returns contents or error

def file_from_url(url):
  try:
    response = requests.get(url, timeout=3)
    return response.text
  except Exception as e:
    return str(e)

#———————————————————————————————————————— weights_to_numbers(txt)

#   accepts a string like FuturaPT-Bold-Obl, and replaces
#   obl by italic, thin by 100 etc.

weight_equivalents = {
  'thin'        : '100',
  'extra-light' : '200',
  'extralight'  : '200',
  'book'        : '400',
  'regular'     : '400',
  'medium'      : '500',
  'demi'        : '600',
  'semi-bold'   : '600',
  'semibold'    : '600',
  'heavy'       : '700',
  'extra-bold'  : '800',
  'extrabold'   : '800',
  'black'       : '900',

  'light'       : '300',
  'bold'        : '700',
}

# receives futura-pt-condensed-extra-bold-italic

def weights_to_numbers(txt):

  results = ''
  for key in weight_equivalents:
    if txt.find(key) > 0:
      txt = txt.replace(key, weight_equivalents[key])

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
