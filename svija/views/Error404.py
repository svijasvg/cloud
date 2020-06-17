#———————————————————————————————————————— 404 error
# https://websiteadvantage.com.au/404-Error-Handler-Checker

# Links folder redirection breaks if the prefix does not exist
# instead of defaulting to en, need to get site default language

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache

from svija.models import Prefix, Settings
from svija.views import PageView

@never_cache
def Error404(request, *args, **kwargs):
#    return HttpResponse("debugging message.")
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
