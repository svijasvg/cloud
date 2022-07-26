#———————————————————————————————————————— SitemapView.py
#
#    see also modules/generate_accessibility.py
#
#    remove XML (1st two lines)
#
#    remove pixel dimensions if present
#    equivalent of checking "responsive" in Illustrator
#
#    add a unique ID based on filename if necessary
#
#    change generic st classes to unique classes
#    based on filename
#
#———————————————————————————————————————— import

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from svija.models import Page, Settings

def SitemapView(request):
  settings = get_object_or_404(Settings,active=True)
  domain = settings.url

  default_code = settings.section.code

  response = sitemap(domain, default_code, Page.objects.all())
  return HttpResponse(response, content_type='text/plain; charset=utf8')

#———————————————————————————————————————— function

def sitemap(domain, default_code, pages):
  results = []

  for page in pages:
    if page.published == True:
      page_code = page.section.code
      if page_code == default_code:
        addr = 'http://'+domain+'/'+page.url
      else:
        addr = 'http://'+domain+'/'+page_code+'/'+page.url

      if page.url != 'missing':
        results.append(addr)

  results = list(dict.fromkeys(results))
  return '\n'.join(results)

#———————————————————————————————————————— fin
