#———————————————————————————————————————— generate_accessibility.py
#
#    see also SitemapView.py
#
#   creates links to all pages to make sure they're crawled correctly
#   includes link to a capture of the home page for social media
#
#———————————————————————————————————————— import

from django.shortcuts import get_object_or_404
from modules.get_accessible import *
from svija.models import Settings

#———————————————————————————————————————— program

def generate_accessibility(domain, pages, page):
  settings = get_object_or_404(Settings,active=True)
  default_code = settings.section.code

  links = prev  = ''

  for this_page in pages.order_by('url'):
    page_code = this_page.section.code

    if page_code == default_code:
      tag = '<a href=http://{0}/{2}>{3}</a> · '
    else:
      tag = '<a href=http://{0}/{1}/{2}>{3}</a> · '

    if this_page.url != 'missing' and this_page.url != prev:
        links += tag.format(domain,page_code,this_page.url,this_page.accessibility_name)
        prev = this_page.url

#———————————————————————————————————————— add capture

  text = get_accessibility(page.accessibility_text)
  capture = '/images/capture.jpg'
  tag = '{0}\n\n{1}<a href=http://{2}><img src={3}></a>'
  results = tag.format(text,links,domain,capture)

  return results

#———————————————————————————————————————— fin
