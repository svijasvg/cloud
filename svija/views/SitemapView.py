#———————————————————————————————————————— SitemapView.py
#
#        remove XML (1st two lines)
#
#        remove pixel dimensions if present
#        equivalent of checking "responsive" in Illustrator
#
#        add a unique ID based on filename if necessary
#
#        change generic st classes to unique classes
#        based on filename
#
#———————————————————————————————————————— import

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from svija.models import Settings, Page

def SitemapView(request):
    settings = get_object_or_404(Settings,active=True)
    domain = settings.url
    response = sitemap(domain, Page.objects.all())
    return HttpResponse(response, content_type='text/plain; charset=utf8')

#———————————————————————————————————————— function

def sitemap(domain, pages):
    results = []
    for page in pages:
        if page.published == True:
          prefix = page.language.code
          if page.url != 'missing':
              results.append('http://'+domain+'/'+prefix+'/'+page.url)

    results = list(dict.fromkeys(results))
    return '\n'.join(results)

#———————————————————————————————————————— fin
