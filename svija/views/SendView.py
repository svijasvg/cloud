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

# from modules import send_mail       
from django.core.mail import send_mail

#———————————————————————————————————————— send mail

def SendView(request):

  if not request.user.is_superuser:
    response = HttpResponse("<h1>Error 404</h1>\nPage not found.")
    response.status_code = 404
    return response

  settings = get_object_or_404(Settings, enabled=True)
  to       = request.GET.get('to', '')

  if to == '':
    response =  "<pre>\n\n    Please include an email address:\n\n      " + settings.url + "/send?to=somebody@example.com&bcc=somebodyelse@website.com\n\n    bcc is optional"
    return HttpResponse(response)

  subject  = "⚠️ test email from " + settings.url
  body   = 'If you have received this message, your Svija email is working' 
  frm    = ''
  cc     = ''
  bcc    = request.GET.get('bcc', '')
  from_email     = "noreply@mail.svija.dev"
  recipient_list = [request.GET.get('to', '')]
  fail_silently  = False

  response = send_mail(subject, body, from_email, recipient_list, fail_silently,)

  if (response == 1):
    return HttpResponse("<pre>\n\n\n    Mail Sent.")
  else:
    return HttpResponse("Error: " + str(response))

#———————————————————————————————————————— older content

# response = send_mail.send(settings, subject, body, frm, [to], [cc], [bcc],)

# if response == '': response = 'mail sent successfully'
# response = '<html><body><pre>\n\n    ' + str(response)

# return HttpResponse(response)

#———————————————————————————————————————— fin

