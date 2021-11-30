#———————————————————————————————————————— MailView.py

#———————————————————————————————————————— notes
#
#   accepts three POST variables
#
#   name   email   message
#
#   returns '' if successful
#
#   E0 = missing email or message
#   E1 = email failes whitelist
#   E2 = name failed blacklist
#   E3 = body failed blacklist
#
#———————————————————————————————————————— import

import re
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from svija.models import Language, Settings
from modules import send_mail

#———————————————————————————————————————— MailView(request):

def MailView(request):

  # comment out these lines for testing

  if request.method != 'POST':
    response = HttpResponse(0)
    response.status_code = 404
    return response

  addr = request.POST.get('email').lower()
  naim = str(request.POST.get('name'))
  body = request.POST.get('message')

# addr = "hompty.hooby@freedom.org"
# naim = ""
# body = "me`'ssage body"

#———————————————————————————————————————— setup

  settings = Settings.objects.filter(active=True).first()
  fail = '' # mail will be sent if not '' at end

#———————————————————————————————————————— language


  if 'language' in request.POST:
    furn_code = request.POST.get('language')
    language = Language.objects.filter(code=furn_code).first()
  else:
   language = settings.language

  to       = language.email
  bcc      = language.bcc
  subject  = language.subject

#———————————————————————————————————————— missing fields

  if addr == '' or body=='':
    return HttpResponse('E0')

#———————————————————————————————————————— validate email

  whitelistmail = re.compile("[a-z,0-9,\.,_,-]+\@[a-z,0-9,\.,-]+\.[a-z]+")

  if not whitelistmail.match(addr):
    return HttpResponse('E1')

#———————————————————————————————————————— validate name & body

  blacklist = ".*[\\|\^|\$|\||\*|\+|\[|\{|<|>]+.*"

  if re.match(blacklist, naim):
    return HttpResponse('E2')

  if re.match(blacklist, body):
    return HttpResponse('E3')

#———————————————————————————————————————— get name if not supplied

  name = prettify(naim, addr)

#———————————————————————————————————————— visible "from" address

  frm = settings.url+ ' <' + settings.mail_id + '>'

#———————————————————————————————————————— convert quote to harmless equivalent

  body = re.sub('"', "''", body)
  body = re.sub("'", "’" , body)
  body = re.sub("`", "’" , body)

#———————————————————————————————————————— from info in body

# name is undefined in the following line

  sender_info = language.mail_frm + ' ' + name + ' (' + addr + ')\n\n'
  body = sender_info + body 

#———————————————————————————————————————— send the message

  response = send_mail.send(settings, subject, to, bcc, body)

# if response == '': response = 'mail sent successfully'
# response = '<html><body><pre>\n\n    ' + str(response)

  return HttpResponse(response)


#———————————————————————————————————————— functions

#———————————————————————————————————————— prettify(name, addr):

def prettify(name, addr):

  if name != '': return name

  name, crap = addr.split('@')
  name = re.sub("_", " ", name)
  name = re.sub("\.", " ", name)
  name = name.title() # http://www.codetable.net/Group/miscellaneous-symbols

  return name


#———————————————————————————————————————— fin
