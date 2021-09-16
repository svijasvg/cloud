#———————————————————————————————————————— redirect_if_home.py

#———————————————————————————————————————— redirect if it's a default page (path not shown)
# 
#   there are two possibilities for addresses like / and /en
#
#   the correct address (minimal), handled by HomePageView
#   the incorrect address (/en, /en/home), handled by this function
#
#   if this page should not have a real address, it's redirected to the
#   abbreviated address
#
#   called by views/PageView to redirect urls that
#   are invisible:
#
#   /en    » /
#   /en/home » /
#   /fr/home » /fr
#
#   if this returns '', nothing is done
#   if this returns an address, the correct http redirect
#   is issued by PageView and the page loading process
#   starts over
#
#———————————————————————————————————————— redirect_if_home(request_language_code, request_page, site_default_code, request_language_default_page):

#   this page will cause 302 redirects if we can go up the hierarchy
#
#   /en » /
#   /fr/accueil » /fr
#
#   none of the received variables have slashes
#   /en/home redirects to /, doesn't get to this function

def redirect_if_home(request_path, site_default_code, request_language_default_page):
  
  path_parts = request_path.split('/')

  #                -3     -2     -1
  #            ø   lang   page   screen

  request_language_code = path_parts[-3]
  request_page = path_parts[-2]
  request_path = request_language_code + '/' + request_page

#———————————————————————————————————————— site language default page · /en › /

  test_path_1 = site_default_code + '/'
  if request_path == test_path_1: return '/'

#———————————————————————————————————————— other language default page · /fr/accueil › /fr

  test_path_2 = request_language_code + '/' + request_language_default_page
  if request_path == test_path_2 : return '/' + request_language_code

#———————————————————————————————————————— no match, return ''

  return ''


#———————————————————————————————————————— fin
