#———————————————————————————————————————— SendView.py

#———————————————————————————————————————— comments
#
#   /send?to=andrew@svija.love&bcc=camrias@free.fr
#
#   to send a test email, to make sure that
#   the mail parameters are correct
#
#   sending parameters are drawn from
#   system settings
#
#———————————————————————————————————————— import

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from svija.models import Settings
from modules import send_mail
from django.http import QueryDict

#———————————————————————————————————————— send mail

def SendView(request):

  if not request.user.is_superuser:
    response = HttpResponse(0)
    response.status_code = 404
    return response

  settings = get_object_or_404(Settings, active=True)

  subject  = "⚠️ test email from " + settings.url
  to     = request.GET.get('to', '')
  bcc    = request.GET.get('bcc', '')
  body   = 'If you have received this message, your email is working' 

  if to == '':
    response =  "<pre>\n\n    Please include an email address:\n\n      " + settings.url + "/send?to=somebody@example.com&bcc=somebodyelse@website.com\n\n    bcc is optional"
    return HttpResponse(response)

  response = send_mail.send(settings, subject, to, bcc, body)

  if response == '': response = 'mail sent successfully'
  response = '<html><body><pre>\n\n    ' + str(response)

  return HttpResponse(response)


#———————————————————————————————————————— fin
