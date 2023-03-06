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

#———————————————————————————————————————— get_fonts()

def get_fonts():
  font_objs  = Font.objects.all()
  css_str    = "@font-face {{ font-family:'{}'; src:{}'){}; }}"
  font_css   = ''
  adobe_css   = ''
  adobe_fonts = []
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
          adb_css, adb_name, adb_url, adb_style, adb_weight = get_adobe_css(this_font)

          this_font.family    = adb_name
          this_font.adobe     = adb_css
          this_font.adobe_url = adb_url
          this_font.style     = adb_weight +' '+adb_style

          this_font.save()

        adobe_fonts.append(this_font)
        
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

  # adobe fonts css if necessary

  if len(adobe_fonts) > 0:

    # get comments from first font in list
    adobe_css = get_adobe_comments(adobe_fonts[0].adobe)

    for f in adobe_fonts:
      adobe_css += "\n@font-face { font-family:'"+f.svg_ref + "'; src:url("+f.adobe_url+") format('woff'); }"

  # google fonts link if necessary
  if len(google_fonts) > 0:
    link_str = '  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family={}">'
    google_link = link_str.format(('|').join(google_fonts))


  return google_link, adobe_css+font_css


#:::::::::::::::::::::::::::::::::::::::: adobe font methods

#———————————————————————————————————————— get_adobe_css(this_font)

# user pastes a string like
#
# <link rel="stylesheet" href="https://use.typekit.net/jpl1zaz.css">
# function returns url of woff file

def get_adobe_css(this_font):

  debug = 'working'

  if this_font.adobe[0] != '<': return this_font.adobe

  #—————————————————————————————————————— get url then CSS file

  bits = this_font.adobe.split('"') # <link rel="stylesheet" href="https://use.typekit.net/jpl1zaz.css">
  url = bits[3]

  response = requests.get(url)
  css_file = response.text

  if css_file[0:2] != '/*':
    return 'URL returned error: '+url+'\n\n'+this_font.adobe, ''

  #—————————————————————————————————————— find match for font

  css_fonts = font_list_from_css(css_file)

  indx        = 0
  best_value  = 0
  best_choice = 0

  target_font = add_dashes(this_font.svg_ref) # returns acier-bat-text-gris

# debug = target_font # futura-pt-extra-bold

# target_font += weights_to_numbers(target_font)
  target_font = weights_to_numbers(target_font)
  target_font = clean_styles(target_font)

  debug = target_font # futura-pt-extra-bold

  for font in css_fonts:

    candidate  = (font['name'] + '-' + font['style'] + '-' + font['weight']).lower()

    v  = match_count(target_font, candidate)
    v += italics_present(target_font, candidate) # remove a point if only candidate has italic

    if v > best_value:
      best_choice = indx
      best_value  = v

    indx += 1

  chosen_font = '/* Found below: ' + css_fonts[best_choice]['name'] + ' • ' + css_fonts[best_choice]['weight'] + ' • ' + css_fonts[best_choice]['style'] + ' */\n\n'

  return chosen_font+css_file, css_fonts[best_choice]['name'], css_fonts[best_choice]['woff'], css_fonts[best_choice]['style'], css_fonts[best_choice]['weight']

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

#———————————————————————————————————————— match_count(arr1, arr2)

def match_count(str1, str2):

  arr1 = str1.lower().split('-')
  arr2 = str2.lower().split('-')

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

#———————————————————————————————————————— italics_present(txt1, txt2)

def italics_present(targ, cand):

  if cand.find('italic') > 0:
     if targ.find('italic') < 1:
       return -1

  return 0

#———————————————————————————————————————— get_adobe_comments(css)

def get_adobe_comments(css):
  start = css.find('/*\n')
  end   = css.find('"}*/\n') + 4
  return css[start:end] + '\n'


#———————————————————————————————————————— fin

#   /* Found below: futura-pt 700 normal */

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
#    * futura-pt:
#    *   - http://typekit.com/eulas/00000000000000000001008f
#    *   - http://typekit.com/eulas/000000000000000000010090
#    *   - http://typekit.com/eulas/000000000000000000010091
#    *   - http://typekit.com/eulas/000000000000000000010092
#    *   - http://typekit.com/eulas/000000000000000000010093
#    *   - http://typekit.com/eulas/000000000000000000013365
#    *   - http://typekit.com/eulas/000000000000000000010095
#    *   - http://typekit.com/eulas/000000000000000000010096
#    *   - http://typekit.com/eulas/000000000000000000010097
#    *   - http://typekit.com/eulas/000000000000000000010098
#    *   - http://typekit.com/eulas/000000000000000000012192
#    *   - http://typekit.com/eulas/000000000000000000012193
#    * futura-pt-condensed:
#    *   - http://typekit.com/eulas/000000000000000000012039
#    *   - http://typekit.com/eulas/00000000000000000001203a
#    *   - http://typekit.com/eulas/00000000000000000001203b
#    *   - http://typekit.com/eulas/00000000000000000001203c
#    *   - http://typekit.com/eulas/00000000000000000001203d
#    *   - http://typekit.com/eulas/00000000000000000001203e
#    *   - http://typekit.com/eulas/00000000000000000001203f
#    *   - http://typekit.com/eulas/000000000000000000012040
#    *
#    * © 2009-2022 Adobe Systems Incorporated. All Rights Reserved.
#    */
#   /*{"last_published":"2023-03-06 08:59:08 UTC"}*/
#   
#   @import url("https://p.typekit.net/p.css?s=1&k=jpl1zaz&ht=tk&f=534.10879.10880.10881.10882.10883.10884.10885.10886.10887.10888.15586.15587.15357.15358.15359.15360.15361.15362.15363.15364.27707&a=24326271&app=typekit&e=css");
#   
#   @font-face {
#   font-family:"abigail";
#   src:url("https://use.typekit.net/af/502479/0000000000000000773596e9/30/l?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n4&v=3") format("woff2"),url("https://use.typekit.net/af/502479/0000000000000000773596e9/30/d?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n4&v=3") format("woff"),url("https://use.typekit.net/af/502479/0000000000000000773596e9/30/a?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n4&v=3") format("opentype");
#   font-display:auto;font-style:normal;font-weight:400;font-stretch:normal;
#   }
#   
#   @font-face {
#   font-family:"futura-pt";
#   src:url("https://use.typekit.net/af/2cd6bf/00000000000000000001008f/27/l?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=n5&v=3") format("woff2"),url("https://use.typekit.net/af/2cd6bf/00000000000000000001008f/27/d?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=n5&v=3") format("woff"),url("https://use.typekit.net/af/2cd6bf/00000000000000000001008f/27/a?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=n5&v=3") format("opentype");
#   font-display:auto;font-style:normal;font-weight:500;font-stretch:normal;
#   }
#   
#   @font-face {
#   font-family:"futura-pt";
#   src:url("https://use.typekit.net/af/1eb35a/000000000000000000010090/27/l?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=i5&v=3") format("woff2"),url("https://use.typekit.net/af/1eb35a/000000000000000000010090/27/d?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=i5&v=3") format("woff"),url("https://use.typekit.net/af/1eb35a/000000000000000000010090/27/a?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=i5&v=3") format("opentype");
#   font-display:auto;font-style:italic;font-weight:500;font-stretch:normal;
#   }
#   
#   @font-face {
#   font-family:"futura-pt";
#   src:url("https://use.typekit.net/af/309dfe/000000000000000000010091/27/l?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=n7&v=3") format("woff2"),url("https://use.typekit.net/af/309dfe/000000000000000000010091/27/d?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=n7&v=3") format("woff"),url("https://use.typekit.net/af/309dfe/000000000000000000010091/27/a?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=n7&v=3") format("opentype");
#   font-display:auto;font-style:normal;font-weight:700;font-stretch:normal;
#   }
#   
#   @font-face {
#   font-family:"futura-pt";
#   src:url("https://use.typekit.net/af/eb729a/000000000000000000010092/27/l?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=i7&v=3") format("woff2"),url("https://use.typekit.net/af/eb729a/000000000000000000010092/27/d?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=i7&v=3") format("woff"),url("https://use.typekit.net/af/eb729a/000000000000000000010092/27/a?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=i7&v=3") format("opentype");
#   font-display:auto;font-style:italic;font-weight:700;font-stretch:normal;
#   }
#   
#   @font-face {
#   font-family:"futura-pt";
#   src:url("https://use.typekit.net/af/849347/000000000000000000010093/27/l?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=i3&v=3") format("woff2"),url("https://use.typekit.net/af/849347/000000000000000000010093/27/d?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=i3&v=3") format("woff"),url("https://use.typekit.net/af/849347/000000000000000000010093/27/a?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=i3&v=3") format("opentype");
#   font-display:auto;font-style:italic;font-weight:300;font-stretch:normal;
#   }
#   
#   @font-face {
#   font-family:"futura-pt";
#   src:url("https://use.typekit.net/af/9b05f3/000000000000000000013365/27/l?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=n4&v=3") format("woff2"),url("https://use.typekit.net/af/9b05f3/000000000000000000013365/27/d?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=n4&v=3") format("woff"),url("https://use.typekit.net/af/9b05f3/000000000000000000013365/27/a?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=n4&v=3") format("opentype");
#   font-display:auto;font-style:normal;font-weight:400;font-stretch:normal;
#   }
#   
#   @font-face {
#   font-family:"futura-pt";
#   src:url("https://use.typekit.net/af/cf3e4e/000000000000000000010095/27/l?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=i4&v=3") format("woff2"),url("https://use.typekit.net/af/cf3e4e/000000000000000000010095/27/d?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=i4&v=3") format("woff"),url("https://use.typekit.net/af/cf3e4e/000000000000000000010095/27/a?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=i4&v=3") format("opentype");
#   font-display:auto;font-style:italic;font-weight:400;font-stretch:normal;
#   }
#   
#   @font-face {
#   font-family:"futura-pt";
#   src:url("https://use.typekit.net/af/ae4f6c/000000000000000000010096/27/l?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=n3&v=3") format("woff2"),url("https://use.typekit.net/af/ae4f6c/000000000000000000010096/27/d?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=n3&v=3") format("woff"),url("https://use.typekit.net/af/ae4f6c/000000000000000000010096/27/a?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=n3&v=3") format("opentype");
#   font-display:auto;font-style:normal;font-weight:300;font-stretch:normal;
#   }
#   
#   @font-face {
#   font-family:"futura-pt";
#   src:url("https://use.typekit.net/af/0c71d1/000000000000000000010097/27/l?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=n8&v=3") format("woff2"),url("https://use.typekit.net/af/0c71d1/000000000000000000010097/27/d?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=n8&v=3") format("woff"),url("https://use.typekit.net/af/0c71d1/000000000000000000010097/27/a?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=n8&v=3") format("opentype");
#   font-display:auto;font-style:normal;font-weight:800;font-stretch:normal;
#   }
#   
#   @font-face {
#   font-family:"futura-pt";
#   src:url("https://use.typekit.net/af/648f69/000000000000000000010098/27/l?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=i8&v=3") format("woff2"),url("https://use.typekit.net/af/648f69/000000000000000000010098/27/d?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=i8&v=3") format("woff"),url("https://use.typekit.net/af/648f69/000000000000000000010098/27/a?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=i8&v=3") format("opentype");
#   font-display:auto;font-style:italic;font-weight:800;font-stretch:normal;
#   }
#   
#   @font-face {
#   font-family:"futura-pt";
#   src:url("https://use.typekit.net/af/c4c302/000000000000000000012192/27/l?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=n6&v=3") format("woff2"),url("https://use.typekit.net/af/c4c302/000000000000000000012192/27/d?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=n6&v=3") format("woff"),url("https://use.typekit.net/af/c4c302/000000000000000000012192/27/a?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=n6&v=3") format("opentype");
#   font-display:auto;font-style:normal;font-weight:600;font-stretch:normal;
#   }
#   
#   @font-face {
#   font-family:"futura-pt";
#   src:url("https://use.typekit.net/af/1b297b/000000000000000000012193/27/l?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=i6&v=3") format("woff2"),url("https://use.typekit.net/af/1b297b/000000000000000000012193/27/d?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=i6&v=3") format("woff"),url("https://use.typekit.net/af/1b297b/000000000000000000012193/27/a?primer=7fa3915bdafdf03041871920a205bef951d72bf64dd4c4460fb992e3ecc3a862&fvd=i6&v=3") format("opentype");
#   font-display:auto;font-style:italic;font-weight:600;font-stretch:normal;
#   }
#   
#   @font-face {
#   font-family:"futura-pt-condensed";
#   src:url("https://use.typekit.net/af/6f8764/000000000000000000012039/27/l?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n4&v=3") format("woff2"),url("https://use.typekit.net/af/6f8764/000000000000000000012039/27/d?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n4&v=3") format("woff"),url("https://use.typekit.net/af/6f8764/000000000000000000012039/27/a?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n4&v=3") format("opentype");
#   font-display:auto;font-style:normal;font-weight:400;font-stretch:normal;
#   }
#   
#   @font-face {
#   font-family:"futura-pt-condensed";
#   src:url("https://use.typekit.net/af/082b7c/00000000000000000001203a/27/l?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=i4&v=3") format("woff2"),url("https://use.typekit.net/af/082b7c/00000000000000000001203a/27/d?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=i4&v=3") format("woff"),url("https://use.typekit.net/af/082b7c/00000000000000000001203a/27/a?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=i4&v=3") format("opentype");
#   font-display:auto;font-style:italic;font-weight:400;font-stretch:normal;
#   }
#   
#   @font-face {
#   font-family:"futura-pt-condensed";
#   src:url("https://use.typekit.net/af/accb3b/00000000000000000001203b/27/l?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n5&v=3") format("woff2"),url("https://use.typekit.net/af/accb3b/00000000000000000001203b/27/d?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n5&v=3") format("woff"),url("https://use.typekit.net/af/accb3b/00000000000000000001203b/27/a?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n5&v=3") format("opentype");
#   font-display:auto;font-style:normal;font-weight:500;font-stretch:normal;
#   }
#   
#   @font-face {
#   font-family:"futura-pt-condensed";
#   src:url("https://use.typekit.net/af/c9ec0c/00000000000000000001203c/27/l?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=i5&v=3") format("woff2"),url("https://use.typekit.net/af/c9ec0c/00000000000000000001203c/27/d?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=i5&v=3") format("woff"),url("https://use.typekit.net/af/c9ec0c/00000000000000000001203c/27/a?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=i5&v=3") format("opentype");
#   font-display:auto;font-style:italic;font-weight:500;font-stretch:normal;
#   }
#   
#   @font-face {
#   font-family:"futura-pt-condensed";
#   src:url("https://use.typekit.net/af/64e0cf/00000000000000000001203d/27/l?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n7&v=3") format("woff2"),url("https://use.typekit.net/af/64e0cf/00000000000000000001203d/27/d?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n7&v=3") format("woff"),url("https://use.typekit.net/af/64e0cf/00000000000000000001203d/27/a?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n7&v=3") format("opentype");
#   font-display:auto;font-style:normal;font-weight:700;font-stretch:normal;
#   }
#   
#   @font-face {
#   font-family:"futura-pt-condensed";
#   src:url("https://use.typekit.net/af/e6a9c1/00000000000000000001203e/27/l?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=i7&v=3") format("woff2"),url("https://use.typekit.net/af/e6a9c1/00000000000000000001203e/27/d?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=i7&v=3") format("woff"),url("https://use.typekit.net/af/e6a9c1/00000000000000000001203e/27/a?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=i7&v=3") format("opentype");
#   font-display:auto;font-style:italic;font-weight:700;font-stretch:normal;
#   }
#   
#   @font-face {
#   font-family:"futura-pt-condensed";
#   src:url("https://use.typekit.net/af/3b8138/00000000000000000001203f/27/l?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n8&v=3") format("woff2"),url("https://use.typekit.net/af/3b8138/00000000000000000001203f/27/d?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n8&v=3") format("woff"),url("https://use.typekit.net/af/3b8138/00000000000000000001203f/27/a?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n8&v=3") format("opentype");
#   font-display:auto;font-style:normal;font-weight:800;font-stretch:normal;
#   }
#   
#   @font-face {
#   font-family:"futura-pt-condensed";
#   src:url("https://use.typekit.net/af/6b4d7c/000000000000000000012040/27/l?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=i8&v=3") format("woff2"),url("https://use.typekit.net/af/6b4d7c/000000000000000000012040/27/d?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=i8&v=3") format("woff"),url("https://use.typekit.net/af/6b4d7c/000000000000000000012040/27/a?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=i8&v=3") format("opentype");
#   font-display:auto;font-style:italic;font-weight:800;font-stretch:normal;
#   }
#   
#   @font-face {
#   font-family:"acier-bat-gris";
#   src:url("https://use.typekit.net/af/b2b981/00000000000000007735dfaf/30/l?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n4&v=3") format("woff2"),url("https://use.typekit.net/af/b2b981/00000000000000007735dfaf/30/d?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n4&v=3") format("woff"),url("https://use.typekit.net/af/b2b981/00000000000000007735dfaf/30/a?primer=7cdcb44be4a7db8877ffa5c0007b8dd865b3bbc383831fe2ea177f62257a9191&fvd=n4&v=3") format("opentype");
#   font-display:auto;font-style:normal;font-weight:400;font-stretch:normal;
#   }
#   
#   .tk-abigail { font-family: "abigail",sans-serif; }
#   .tk-futura-pt { font-family: "futura-pt",sans-serif; }
#   .tk-futura-pt-condensed { font-family: "futura-pt-condensed",sans-serif; }
#   .tk-acier-bat-gris { font-family: "acier-bat-gris",sans-serif; }
#   
