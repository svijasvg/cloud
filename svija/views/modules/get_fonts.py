#———————————————————————————————————————— get_fonts.py

#———————————————————————————————————————— notes
#
# should be first in CSS
# by default all fonts are included
# svg_cleaner adds fonts only if they're not already in DB
#
# if there's a global list of fonts in PageView
# svg cleaner can add to it
# and this function can use it IF it's after svg cleaner
#
#———————————————————————————————————————— imports

from svija.models import Font
import requests

def get_fonts():

  font_objs  = Font.objects.all()
  css_str    = "@font-face {{ font-family:'{}'; src:{}'){}; }}"
  font_css   = ''
  google_fonts = []
  google_link  = ''

  for this_font in font_objs:
    if this_font.enabled:
      svg_ref = this_font.svg_ref
      font_src  = this_font.woff

      # remove everything in beginning of path if necessary
      # /Users/Main/Library/Mobile Documents/com~apple~CloudDocs/Desktop/svija.dev/sync/Svija/Fonts/Woff Files/clarendon.woff
    
      if font_src.find('/') > -1:
        font_src = font_src.rpartition("/")[2]
        this_font.woff = font_src
        this_font.save()

      # adobe fonts
      if this_font.adobe != '':
        if this_font.adobe[0] == '<':
          adb_css, adb_url, adb_style, adb_weight = get_adobe_css(this_font)

          this_font.adobe = adb_css
          this_font.adobe_url = adb_url
          this_font.style = adb_weight +' '+adb_style

          this_font.save()
        
      # google fonts
      elif this_font.google:
        req = this_font.style.lower().replace(' ','')
        req = this_font.family.replace(' ','+') + ':' + req 
        google_fonts.append(req)

      # woff2 and woff fonts
      elif font_src.find('woff2') > 0:
        font_format = " format('woff2')"
        font_src = "url('/fonts/" + font_src
        font_css  += '\n'+ css_str.format(svg_ref, font_src, font_format)

      elif font_src.find('woff') > 0:  
        font_format = " format('woff')"
        font_src = "url('/fonts/" + font_src
        font_css += '\n'+ css_str.format(svg_ref, font_src, font_format)

      # local fonts
      elif font_src.find(',') > 0: # local fonts
        # src: local('Arial'), local('Arial MT'), local('Arial Regular'); }
        font_format = ''
        locals = font_src.replace(', ',',').split(',')
        font_src = "local('"+"'), local('".join(locals)
        font_css += '\n'+ css_str.format(svg_ref, font_src, font_format)


  if len(google_fonts) > 0:
    link_str = '  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family={}">'
    google_link = link_str.format(('|').join(google_fonts))

  return google_link, font_css


#:::::::::::::::::::::::::::::::::::::::: methods

#———————————————————————————————————————— get_names_woffs(this_font)
#
#   returns list of fonts found in css
#
#   each font contains:
#   - name: family name
#   - woff: source
#   - style
#   - weight
#
#   - name1, name2:     start & end indexes
#   - woff1, woff2:     start & end indexes
#   - style1, style2:   start & end indexes
#   - weight1, weight2: start & end indexes

def get_names_woffs(css_contents):

#———————————————————————————————————————— initialise

  font_list = []
  start_index = 0

  how_many = int(css_contents.count('font-face')) # because each font is listed once with source, then once with class

  for x in range(how_many):

    #———————————————————————————————————— get family indexes
  
    this_adobe  = {}
  
    name_first = css_contents.find('font-family', start_index) + 13
    name_last  = css_contents.find('"', name_first)
  
    this_adobe['name1'] = name_first
    this_adobe['name2'] = name_last
    this_adobe['name']  = css_contents[name_first:name_last]
  
    #———————————————————————————————————— get woff indexes
  
    woff_first = css_contents.find('url("', name_last) + 5
    woff_last  = css_contents.find('")', woff_first)
  
    this_adobe['woff1'] = woff_first
    this_adobe['woff2'] = woff_last
    this_adobe['woff']  = css_contents[woff_first:woff_last]
  
    #———————————————————————————————————— get style indexes
  
    style_first = css_contents.find('font-style:', name_last) + 11
    style_last  = css_contents.find(';', style_first)
  
    this_adobe['style1'] = style_first
    this_adobe['style2'] = style_last
    this_adobe['style']  = css_contents[style_first:style_last]
  
    #———————————————————————————————————— get weight indexes
  
    weight_first = css_contents.find('font-weight:', name_last) + 12
    weight_last  = css_contents.find(';', weight_first)
  
    this_adobe['weight1'] = weight_first
    this_adobe['weight2'] = weight_last
    this_adobe['weight']  = css_contents[weight_first:weight_last]
  

    #———————————————————————————————————— add font to list

    font_list.append(this_adobe)
    start_index = style_last

  return font_list

#———————————————————————————————————————— name_splitter(txt)
#
#   splits a name into an array
#   - if this char is space, replace with -
#   - if this char is lower & next is upper, add - between them
#   - if this car is upper & prev is upper & next is lower, add - after this char
#
#   split at each -

def name_splitter(txt):
  
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

  return dashes.split('-')

#———————————————————————————————————————— adobe font handler

# <link rel="stylesheet" href="https://use.typekit.net/jpl1zaz.css">

def get_adobe_css(this_font):

  if this_font.adobe[0] != '<': return this_font.adobe

  zopy = this_font.adobe
  zname = this_font.family
  zstyle = this_font.style

  #—————————————————————————————————————— get Adobe CSS source
  
  # <link rel="stylesheet" href="https://use.typekit.net/jpl1zaz.css">

  bits = zopy.split('"')
  url = bits[3]
  response = requests.get(url)
  css_source = response.text

  #—————————————————————————————————————— error handling

  if css_source[0:2] != '/*':
    return 'URL returned error: '+url+'\n\n'+zopy, ''

  #—————————————————————————————————————— get fonts found in this css

  listed_in_css = get_names_woffs(css_source)

  #—————————————————————————————————————— if there's only one, return it

  if len(listed_in_css) == 1:
    return css_source, listed_in_css[0]['woff']

  #—————————————————————————————————————— find match for font

  compare_to = name_splitter(this_font.svg_ref) # convert svg name into bits
  # returns acier · bat · text · gris

  indx        = 0
  best_value  = 0
  best_choice = 0

  debug = ''

  for adobe_font in listed_in_css:
    to_compare = adobe_font['name'].split('-')

    v = match_count(compare_to, to_compare)
    debug += ':'+str(v)+':'+adobe_font['name']
    if v > best_value:
      best_choice = indx
      best_value  = v

    indx += 1

  chosen_font = '/* Found below: '+listed_in_css[best_choice]['name']+' */\n\n'

  return chosen_font+css_source, listed_in_css[best_choice]['woff'], listed_in_css[best_choice]['style'], listed_in_css[best_choice]['weight']

#———————————————————————————————————————— match_count(arr1, arr2)

def match_count(arr1, arr2):

  len_1 = len(arr1)
  len_2 = len(arr2)

  if len_1 > len_2:
    cent   = len_1
    first  = arr1
    second = arr2
  else:
    cent   = len_2
    first  = arr2
    second = arr1

  matches = 0

  for element1 in first:
    for element2 in second:
      if element1 == element2:
        matches += 1
  
  return matches


#———————————————————————————————————————— fin

#   <link rel="stylesheet" href="https://use.typekit.net/jpl1zaz.css">

#   SVG name: AcierBATText-Gris

#   /*
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

