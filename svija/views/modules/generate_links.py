#———————————————————————————————————————— generate_links.py

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

# accessible = generate_links(settings.url, Page.objects.all(), page)

def generate_links(url, pages, page):

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
      tag = '<a alt="{4}" href=http://{0}/{2}>{3}</a> · '       # exclude section

    # if we DO need to include section in url
    else:
      tag = '<a alt="{4}" href="http://{0}/{1}{2}">{3}</a> · ' # include section

    name = this_page.accessibility_name
    if name == '': name = 'link'

#———————————————————————————————————————— add any pages that aren't dupes (cp/mb) or "missing"

    if this_page.url != 'missing' and this_page.url != prev:

        if this_page.url == this_page.section.default_page:
          links += tag.format(url, page_section_code, '', name, this_page.title)

        elif page_section_code == active_section:
          links += tag.format(url, page_section_code+'/', this_page.url, name, this_page.title)

#———————————————————————————————————————— keep url to exclude from next cycle

        prev = this_page.url

#———————————————————————————————————————— add capture

  capture = '/images/capture.jpg'
  tag = '<a href=http://{0}><img src={1}></a>'
  capture_tag = tag.format(url,capture)

  return links, capture_tag


#———————————————————————————————————————— fin
