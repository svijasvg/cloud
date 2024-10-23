
#:::::::::::::::::::::::::::::::::::::::: views/modules/screen_redirect_js.py

#———————————————————————————————————————— notes
#
#   will include JS to reload page is screen size is wrong
#
#   ONLY if user agent doesn't contain 'google'
#
#———————————————————————————————————————— imports

import re

#:::::::::::::::::::::::::::::::::::::::: definition

def screen_redirect_js(ua):

  str = 'google'

  if re.search(str, ua, re.IGNORECASE):
    return ''

  code = 'if (cookiesEnabled()) if (screen_code != correct_code) window.location.replace(document.URL)'

  return code

#:::::::::::::::::::::::::::::::::::::::: functions



def not_google(ua):

  # https://stackoverflow.com/questions/6579876/how-to-match-a-substring-in-a-string-ignoring-case

  if re.search('google', ua, re.IGNORECASE):
    return 'false'

  return 'true'


#:::::::::::::::::::::::::::::::::::::::: fin
