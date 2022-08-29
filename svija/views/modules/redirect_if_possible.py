#———————————————————————————————————————— redirect_if_possible.py

#   DO NOT REDIRECT IF PAGE IS CALLED MISSING

#———————————————————————————————————————— notes
#
#   called by the main page view to redirect if the slugs should be hidden
#
#   each page can have 1 or two slugs:
#
#   slug1 = section or page
#   slug2 = page
#
#   if a section is the default for the site, then it shouldn't be visible
#   if a page is the default for a section, then it shouldn't be visible
#
#   returns '' if no redirect is needed
#   otherwise returns the new URL
#   PageView will then issue a 302 redirect
#
#   return HttpResponse("debugging message.")
#
#   wrong screen code is handled separately, because
#   this will issue a 302 redirect, and we don't want
#   to redirect to the same URL
#
#———————————————————————————————————————— redirect_if_possible(request, section_code, default_page):

def redirect_if_possible(request, section_code, default_page):

# return request.path # /main/kds

  whole_path  = request.path[1:]   # ignore leading slash
  path_parts = whole_path.split('/');

#———————————————————————————————————————— remove page if default

  page = len(path_parts) - 1

  if len(path_parts)>0 and path_parts[page] == default_page:
    del path_parts[page]

#———————————————————————————————————————— remove section if default

  if len(path_parts)>0 and path_parts[0]==section_code:
    del path_parts[0]

#———————————————————————————————————————— return results

  new_path = '/'.join(path_parts)

  if new_path != whole_path: return '/' + new_path
  else: return False


#———————————————————————————————————————— fin
