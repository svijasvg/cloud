#   return HttpResponse("debugging message.")
#———————————————————————————————————————— 404 error
# https://websiteadvantage.com.au/404-Error-Handler-Checker

# Links folder redirection breaks if the prefix does not exist
# instead of defaulting to en, need to get site default language

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache

from svija.models import Forwards, Prefix, Settings
from svija.views import PageView

@never_cache
def Error404(request, *args, **kwargs):

    requested = request.path[1:]

    #———————————————————————————————————————— check fer redirect

    # 3 cases:
    # external site, starts with http or https
    # internal address, with prefix like /fr/
    # internal address, with no prefix like /admin/svija/help/

    try:
        redirect_obj = Forwards.objects.get(from_url=requested, active=True)

        if redirect_obj.to_prefix[0:4] == 'http': # or https
            return HttpResponsePermanentRedirect(redirect_obj.to_prefix + '://' + redirect_obj.to_page)
        elif redirect_obj.to_prefix != '':
            return HttpResponsePermanentRedirect('/'+redirect_obj.to_prefix + '/' + redirect_obj.to_page)
        else:
            return HttpResponsePermanentRedirect('' + redirect_obj.to_page)

    except ObjectDoesNotExist: pass

    # get prefix if possible, otherwise get site default prefix

    path1 = request.path.split('/')[1]
    try:
        prefix = Prefix.objects.get(path=path1)
    except ObjectDoesNotExist:
        settings = get_object_or_404(Settings,active=True)
        path1 = settings.prefix.path

    response = PageView(request, path1, 'missing',)
    response.status_code = 404
    return response

#———————————————————————————————————————— fin
