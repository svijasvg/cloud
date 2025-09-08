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
from django.core.mail import EmailMessage
from django.core.mail import send_mail

#———————————————————————————————————————— send mail

def SendView(request):

  if not request.user.is_superuser:
    response = HttpResponse("<h1>Error 404</h1>\nPage not found.")
    response.status_code = 404
    return response

  #———————————————————— necessary to get host name

  settings = get_object_or_404(Settings, enabled=True)

  #———————————————————— validate to address

  to       = request.GET.get('to', '')

  if to == '':
    response =  "<pre>\n\n    Please include an email address:\n\n      " + settings.url + "/send?to=somebody@example.com&bcc=somebodyelse@website.com\n\n    bcc is optional"
    return HttpResponse(response)

  #———————————————————— organize content

  subject        = "⚠️ test email from " + settings.url
  body           = 'Your Svija email is working' 
  cc             = ''
  bcc            = request.GET.get('bcc', '')
  from_email     = "noreply@mail.svija.dev"

  #———————————————————— 

  email = EmailMessage(
      subject=subject,
      body=body,
      from_email=from_email,
      to=[to],          # main recipients
      cc=[cc],          # optional
      bcc=[bcc],        # hidden recipients
  )

  #————————————————————

  response = email.send(fail_silently=False)

  if (response == 1):
    return HttpResponse("<pre>\n\n\n    Mail Sent.")
  else:
    return HttpResponse("Error: " + str(response))

#———————————————————————————————————————— fin

