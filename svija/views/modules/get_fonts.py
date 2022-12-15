#———————————————————————————————————————— get_fonts.py
# should be first in CSS
# by default all fonts are included
# svg_cleaner adds fonts only if they're not already in DB

# if there's a global list of fonts in PageView
# svg cleaner can add to it
# and this function can use it IF it's after svg cleaner

from svija.models import Font
import requests

#ef get_fonts(core_content):
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

      if this_font.adobe != '':
        if this_font.adobe[0] == '<':
          this_font.adobe, this_font.adobe_url = get_adobe_css(this_font.adobe)
          this_font.save()
        
      elif this_font.google:
        req = this_font.style.lower().replace(' ','')
        req = this_font.family.replace(' ','+') + ':' + req 
        google_fonts.append(req)

      elif font_src.find('woff2') > 0:
        font_format = " format('woff2')"
        font_src = "url('/fonts/" + font_src
        font_css  += '\n'+ css_str.format(svg_ref, font_src, font_format)

      elif font_src.find('woff') > 0:  
        font_format = " format('woff')"
        font_src = "url('/fonts/" + font_src
        font_css += '\n'+ css_str.format(svg_ref, font_src, font_format)

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

#———————————————————————————————————————— adobe font handler

# <link rel="stylesheet" href="https://use.typekit.net/jpl1zaz.css">

def get_adobe_css(this_font):

  if this_font[0] != '<':
    return this_font

#———————————————————————————————————————— get Adobe CSS source

  bits = this_font.split('"')
  url = bits[3]
  response = requests.get(url)
  css_source = response.text

#———————————————————————————————————————— 

  this_url = 'working'
  return css_source, this_url

#———————————————————————————————————————— fin

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

