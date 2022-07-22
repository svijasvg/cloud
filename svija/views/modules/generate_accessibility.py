#———————————————————————————————————————— generate_accessibility.py
#
#   creates links to all pages to make sure they're crawled correctly
#   includes link to a capture of the home page for social media
#
#———————————————————————————————————————— import

from modules.get_accessible import *

#———————————————————————————————————————— program

def generate_accessibility(domain, pages, page):
    links = ''
    prev  = ''
    for this_page in pages.order_by('url'):
      prefix = this_page.section.code
      tag = '<a href=http://{0}/{1}/{2}>{3}</a> · '
      if this_page.url != 'missing' and this_page.url != prev:
          links += tag.format(domain,prefix,this_page.url,this_page.accessibility_name)
          prev = this_page.url

#———————————————————————————————————————— add capture

    text = get_accessibility(page.accessibility_text)
    capture = '/images/capture.jpg'
    tag = '{0}\n\n{1}<a href=http://{2}><img src={3}></a>'
    results = tag.format(text,links,domain,capture)

    return results

#———————————————————————————————————————— fin
