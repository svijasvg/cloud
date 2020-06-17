#———————————————————————————————————————— MailView.py

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from svija.models import Prefix, Settings

#———————————————————————————————————————— send mail

from modules import send_mail

def MailView(request, lng):
    if request.method != 'POST': return HttpResponse(0)

    ua = request.META['HTTP_USER_AGENT']

    pfix = get_object_or_404(Prefix, path=lng)
    lng = pfix.language

    settings = get_object_or_404(Settings,active=True)
    response = send_mail.send(settings, lng, request.POST, ua)

    return HttpResponse(response)

#———————————————————————————————————————— fin
