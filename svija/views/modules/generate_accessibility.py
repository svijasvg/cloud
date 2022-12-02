#———————————————————————————————————————— generate_accessibility.py

#———————————————————————————————————————— notes
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

# accessible = generate_accessibility(settings.url, Page.objects.all(), page)

def generate_accessibility(url, pages, page):

  links = prev  = ''

#———————————————————————————————————————— get default section w/code

  settings = get_object_or_404(Settings,enabled=True)
  default_code = settings.section.code
 
  active_section = page.section.code

#———————————————————————————————————————— loop through all pages

  for this_page in pages.order_by('url'):
    page_section_code = this_page.section.code

    # if we don't need to include section in url
    if page_section_code == default_code:
      tag = '<a href=http://{0}/{2}>{3}</a> · '       # exclude section

    # if we DO need to include section in url
    else:
      tag = '<a href="http://{0}/{1}{2}">{3}</a> · ' # include section

    name = this_page.accessibility_name
    if name == '': name = 'link'

#———————————————————————————————————————— add any pages that aren't dupes (cp/mb) or "missing"

    if this_page.url != 'missing' and this_page.url != prev:

        if this_page.url == this_page.section.default_page:
          links += tag.format(url,page_section_code,'',name)

        elif page_section_code == active_section:
          links += tag.format(url,page_section_code+'/',this_page.url,name)

#———————————————————————————————————————— keep url to exclude from next cycle

        prev = this_page.url

#———————————————————————————————————————— add capture

  text = get_accessibility(page.accessibility_text)
  capture = '/images/capture.jpg'
  tag = '{0}\n\n{1}<a href=http://{2}><img src={3}></a>'
  results = tag.format(text,links,url,capture)

  return results


#———————————————————————————————————————— fin
