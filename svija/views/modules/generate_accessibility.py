#---------------------------------------- generate_accessibility.py
#
#   creates links to all pages to make sure they're crawled correctly
#   includes link to a capture of the home page for social media
#
#---------------------------------------- program

def generate_accessibility(domain, pages, page):
    links = ''
    for this_page in pages.order_by('url'):
      prefix = this_page.language.code
      tag = '<a href=http://{0}/{1}/{2}>{3}</a> · '
      if this_page.url != 'missing':
          links += tag.format(domain,prefix,this_page.url,this_page.accessibility_name)

#---------------------------------------- add capture

    text = page.accessibility_text
    capture = '/images/capture.jpg'
    tag = '{0}\n\n{1}<a href=http://{2}><img src={3}></a>'
    results = tag.format(text,links,domain,capture)

    return results

#---------------------------------------- fin
