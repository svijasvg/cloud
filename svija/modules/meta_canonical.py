#---------------------------------------- canonical.py
# inserts results: <meta [results] >
import os
from django.db.models import Q
from svija.models import Prefix

def create_canonical(prefix, responsive, language, host,dir, url):

#----------------------------------------- find the correct prefix for the link

    is_canonical = responsive.canonical
    meta_tag = responsive.meta_tag

#----------------------------------------- find the correct prefix for the link
# right now it just takes anything that's different
# should look for canonical if it's not canonical

    all_prefix = Prefix.objects.filter(Q(language=language)&~Q(responsive=responsive))
    new_prefix = all_prefix[0]

#----------------------------------------- the easy part

    tag = responsive.meta_tag + ' href="http://{0}/{1}/{2}"'
    tag = tag.format(host,new_prefix,url)
    return tag

#----------------------------------------- fin

