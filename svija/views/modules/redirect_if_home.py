#————————————————————————————————————————  redirect if it's a default page (path not shown)

from django.http import HttpResponsePermanentRedirect

def redirect_if_home(request_prefix, request_path, settings, prefix_default):

    site_default_prefix = '/' + settings.prefix.path +'/'            # default prefix for site
    site_default_slug   = settings.prefix.default                    # default slug for prefix
    site_default_path   = site_default_prefix + site_default_slug    # default slug for prefix

    this_prefix         = '/' + request_prefix +'/'
    this_prefix_default    = this_prefix + prefix_default

    # if address corresponds to site default page
    if request_path == site_default_path or request_path == site_default_prefix: return '/'

    # if address corresponds to prefix default page
    if request_path == this_prefix_default: return this_prefix

    return ''
