#---------------------------------------- generate_accessibility.py
#
#   creates links to all pages to make sure they're crawled correctly
#   includes link to a capture of the home page for social media
#
#---------------------------------------- program

def generate_accessibility(domain, pages, page):
    links = ''
    for page in pages:
        canonical = page.prefix.responsive.canonical
        if canonical==True:
            prefix = page.prefix.path
            tag = '<a href=http://{0}/{1}/{2}>{3}</a> · '
            if page.url != 'missing':
                links += tag.format(domain,prefix,page.url,page.snippet_name)

#---------------------------------------- add capture

    text = page.snippet_text
    capture = '/images/capture.jpg'
    tag = '{0}\n\n{1}<a href=http://{2}><img src={3}></a>'
    results = tag.format(text,links,domain,capture)

    return results

#---------------------------------------- fin
