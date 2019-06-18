#---------------------------------------- accessibility.py
#
#   creates links to all pages to make sure they're crawled correctly
#   includes link to a capture of the home page for social media
#
#---------------------------------------- program

def create(domain, pages):
    results = ''
    for page in pages:
        canonical = page.prefix.responsive.canonical
        if canonical==True:
            prefix = page.prefix.path
            tag = '<a href=http://{0}/{1}/{2}>{3}</a> · '
            if page.url != 'missing':
                results += tag.format(domain,prefix,page.url,page.access_name)

#---------------------------------------- add capture

    return results

#---------------------------------------- fin

