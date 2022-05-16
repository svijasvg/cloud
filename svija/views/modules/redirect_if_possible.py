#———————————————————————————————————————— redirect_if_possible.py

#———————————————————————————————————————— redirect if it's a default page (path not shown)
#
#   called by the main page view to redirect if the slugs should be hidden
#
#   each page can have 1 or two slugs:
#
#   slug1 = language or page
#   slug2 = page
#
#   if a language is the default for the site, then it shouldn't be visible
#   if a page is the default for a language, then it shouldn't be visible
#
#   returns '' if no redirect is needed
#   otherwise returns the new URL
#   PageView will then issue a 302 redirect
#
#    return HttpResponse("debugging message.")
#
#———————————————————————————————————————— redirect_if_possible(request, site_lang, language_page):

def redirect_if_possible(request, site_lang, language_page):

  path_parts = request.path[1:].split('/'); # ignore leading slash

  del path_parts[len(path_parts) - 1]       # remove screen code
  
  orig_path = '/'.join(path_parts)

#———————————————————————————————————————— remove page if default

  page = len(path_parts) - 1

  if len(path_parts)>0 and path_parts[page] == language_page:
    del path_parts[page]

#———————————————————————————————————————— remove language if default

  if len(path_parts)>0 and path_parts[0]==site_lang:
    del path_parts[0]

#———————————————————————————————————————— return results

  new_path = '/'.join(path_parts)

  if new_path != orig_path: return '/' + new_path
  else: return False


#———————————————————————————————————————— fin
