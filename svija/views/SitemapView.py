#———————————————————————————————————————— sitemap.txt

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from svija.models import Settings, Page

from modules import sitemap

def SitemapView(request):
    settings = get_object_or_404(Settings,active=True)
    domain = settings.url
    response = sitemap.create(domain, Page.objects.all())
    return HttpResponse(response, content_type='text/plain; charset=utf8')

#———————————————————————————————————————— fin
