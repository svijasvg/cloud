#---------------------------------------- canonical.py

# inserts results: <meta [results] >
#  <meta rel="alternate" media="only screen and (max-width: 640px)" href="http://ozake.com/em/works" >

import os
from django.db.models import Q
from svija.models import Prefix

def meta_canonical(        responsive, language, secure, host, dir, url):

#----------------------------------------- find the correct prefix for the link

    is_canonical = responsive.canonical
    meta_tag = responsive.meta_tag

#----------------------------------------- find the correct prefix for the link
# right now it just takes anything that's different
# should look for canonical if it's not canonical

#   all_prefix = Prefix.objects.filter(Q(language=language)&~Q(responsive=responsive))
#   new_prefix = all_prefix[0]

#----------------------------------------- the easy part

    protocol = 'https' if secure else 'http'

    tag = responsive.meta_tag + ' href="' + protocol + '://{0}/{1}/{2}"'
    tag = tag.format(host, dir, url)
    return tag

#----------------------------------------- fin

