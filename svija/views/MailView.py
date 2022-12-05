#———————————————————————————————————————— MailView.py

# uses modules/send_mail.py to actually send

#———————————————————————————————————————— notes
#
#   accepts one POST variable: message
#
#   returns '' if successful
#
#   or returns
#   E1 = missing email or message
#   E2 = message failed blacklist
#
#———————————————————————————————————————— import

import re
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404
from svija.models import Section, Settings
from modules import send_mail

#———————————————————————————————————————— MailView(request):

from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpRequest
from django.conf import settings

def MailView(request):
  email = EmailMessage('Hello', 'World', to=['svijalove@hotmail.com'])
  email.send()

  return HttpResponse('worked')

#     settings  = Settings.objects.filter(enabled=True).first()
#     section   = settings.section
#     blacklist = ".*[\\|\^|\$|\||\*|\+|\[|\{|<|>]+.*"
#   
#   #———————————————————————————————————————— check for validity
#   
#     if request.method != 'POST':
#       response = HttpResponse(0)
#       response.status_code = 404
#       return response
#   
#     message = request.POST.get('message')
#   
#     if message=='':
#       return HttpResponse('E1')
#   
#     if re.match(blacklist, message):
#       return HttpResponse('E2')
#   
#   #———————————————————————————————————————— get section from referrer
#   
#     referrer = request.META.get('HTTP_REFERER') # https://svija.love/en/try
#     if referrer.count('/') > 3:
#       parts = referrer.split('/')
#       referring_code = parts[3]
#       ref_section = Section.objects.filter(code=referring_code).first()
#       if type(ref_section) is not type(None):
#         section = ref_section
#   
#   #———————————————————————————————————————— section-dependent parameters
#   
#     to       = section.email
#     bcc      = section.bcc
#     subject  = section.subject
#   
#   #———————————————————————————————————————— multiple recipients uniquely for our own domains
#   # type python3 to get console
#   
#     # referrer = https://svija.dev/access
#     protocol, slash, realDomain, trash  = referrer.split('/',3)
#   
#     domains = ['svija.love', 'svija.dev',]
#     authorized = False
#     
#     for thisDomain in domains:
#       if realDomain == thisDomain:
#         authorized = True
#   
#     if authorized:
#       allLines = message.split('\n');
#       lastLine = allLines[-1]
#   
#       while lastLine[:3]=='to:' or lastLine[:3]=='cc:' or lastLine[:4]=='bcc:':
#         message += '\n FOUND IT'
#         del allLines[-1]
#         lastLine = allLines[-1]
#   
#       message = '\n'.join(allLines)
#   
#   #   while lastLine[0,3] == 'to:' || lastLine[0,3] == 'cc:' || lastLine[0,4] == 'bcc:':
#   #     which = lastLine[0,3]
#   #     switch which:
#   #       case 'to:'; to += lastLine[4]; break
#   #       case 'cc:': cc += lastLine[4]; break
#   #       case 'bcc': bcc += lastLine[5]; break
#   
#   
#   #———————————————————————————————————————— send message
#   
#     message = stripQuotes(message)
#     response = send_mail.send(settings, subject, to, bcc, message)
#     return HttpResponse(response)
#   
#   
#   #———————————————————————————————————————— functions
#   
#   def stripQuotes(str):
#     str = re.sub('"', "''", str)
#     str = re.sub("'", "’" , str)
#     str = re.sub("`", "’" , str)
#     return str
#   
#   
#   #———————————————————————————————————————— fin
