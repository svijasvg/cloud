
# vim: set foldmethod=marker fmr=#—,##:

#:::::::::::::::::::::::::::::::::::::::: views/modules/screen_redirect_js.py

#———————————————————————————————————————— notes
#
#   defined in system js at top of page:
#  
#   var screen_code = "cp"
#   var all_screens = {0:'cp', 400:'mb'}
#
#   correct_code: set by screens_max.js
#
#   —————————————————————————————————————
#
#   three related scripts:
#
#   1. templates/svija/js/screens_max.js
#
#   2. views/modules/screen_redirect_js.py
#
#      if it's a fresh start & page doesn't match
#      correct code, reload page (if not google)
#
#   3. templates/svija/js/cloud_module_max.js 
#
#      sets cookie & localStorage to new screen code 
#      to enable visiting a page with "wrong" code
##
#———————————————————————————————————————— imports

import re
##

#:::::::::::::::::::::::::::::::::::::::: definition

def screen_redirect_js(ua):

  if re.search('google', ua, re.IGNORECASE): return ''

  # new visitor to wrong version
  code = 'if (fresh_start) if (screen_code != correct_code) window.location.replace(document.URL)'

  return code

#:::::::::::::::::::::::::::::::::::::::: fin

