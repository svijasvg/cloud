#---------------------------------------- sitemap.py
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
#---------------------------------------- program

#from .models import Page

# given path to source file & name (need to figure out what to pass exactly)

def create(domain, pages):
    results = ''
    for page in pages:
        if page.visitable == True:
          prefix = page.prefix
          results += '\nhttp://'+domain+'/'+prefix.path+'/'+page.url
    return results


