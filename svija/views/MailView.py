#———————————————————————————————————————— MailView.py
#
#   remove references to address or name
#   sender_info = section.mail_frm + ' ' + name + ' (' + addr + ')\n\n'
#   message = sender_info + message 
#
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
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from svija.models import Section, Settings
from modules import send_mail

#———————————————————————————————————————— MailView(request):

def MailView(request):

  settings  = Settings.objects.filter(enabled=True).first()
  section   = settings.section
  blacklist = ".*[\\|\^|\$|\||\*|\+|\[|\{|<|>]+.*"

#———————————————————————————————————————— check for validity

  if request.method != 'POST':
    response = HttpResponse(0)
    response.status_code = 404
    return response

  message = request.POST.get('message')

  if message=='':
    return HttpResponse('E1')

  if re.match(blacklist, message):
    return HttpResponse('E2')

#———————————————————————————————————————— get section from referrer

  referrer = request.META.get('HTTP_REFERER') # https://svija.love/en/try
  if referrer.count('/') > 3:
    parts = referrer.split('/')
    referring_code = parts[3]
    ref_section = Section.objects.filter(code=referring_code).first()
    if type(ref_section) is not type(None):
      section = ref_section

#———————————————————————————————————————— section-dependent parameters

  to       = section.email
  bcc      = section.bcc
  subject  = section.subject

#———————————————————————————————————————— send message

  message = stripQuotes(message)
  response = send_mail.send(settings, subject, to, bcc, message)
  return HttpResponse(response)


#———————————————————————————————————————— functions

def stripQuotes(str):
  str = re.sub('"', "''", str)
  str = re.sub("'", "’" , str)
  str = re.sub("`", "’" , str)
  return str


#———————————————————————————————————————— fin
