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
#———————————————————————————————————————— documentation
#
#    The EmailMessage class is initialized with the following parameters
#    (in the given order, if positional arguments are used). All parameters are 
#    optional and can be set at any time prior to calling the send() method.
#
#      subject: The subject line of the email.
#         body: The body text. This should be a plain text message.
#   from_email: The sender’s address. Both fred@example.com and "Fred" <fred@example.com> forms are legal. If omitted, the DEFAULT_FROM_EMAIL setting is used.
#           to: A list or tuple of recipient addresses.
#          bcc: A list or tuple of addresses used in the “Bcc” header when sending the email.
#   connection: An email backend instance. Use this parameter if you want to use the same connection for multiple messages. If omitted, a new connection is created when send() is called.
#  attachments: A list of attachments to put on the message. These can be either MIMEBase instances, or (filename, content, mimetype) triples.
#      headers: A dictionary of extra headers to put on the message. The keys are the header name, values are the header values. It’s up to the caller to ensure header names and values are in the correct format for an email message. The corresponding attribute is extra_headers.
#           cc: A list or tuple of recipient addresses used in the “Cc” header when sending the email.
#     reply_to: A list or tuple of recipient addresses used in the “Reply-To” header when sending the email.
#
#———————————————————————————————————————— import

import re
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404
from svija.models import Section, Settings
from modules import send_mail

#———————————————————————————————————————— from send_mail module

import socket
from smtplib import SMTPException
from django.core.mail import get_connection, EmailMessage

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

#———————————————————————————————————————— multiple recipients uniquely for our own domains
# type python3 to get console

  # referrer = https://svija.dev/access
  protocol, slash, realDomain, trash  = referrer.split('/',3)

  domains = ['svija.love', 'svija.dev',]
  authorized = False
  
  for thisDomain in domains:
    if realDomain == thisDomain:
      authorized = True

  if authorized:
    allLines = message.split('\n');
    lastLine = allLines[-1]

    while lastLine[:3]=='to:' or lastLine[:3]=='cc:' or lastLine[:4]=='bcc:':
      message += '\n FOUND IT'
      del allLines[-1]
      lastLine = allLines[-1]

    message = '\n'.join(allLines)

#   while lastLine[0,3] == 'to:' || lastLine[0,3] == 'cc:' || lastLine[0,4] == 'bcc:':
#     which = lastLine[0,3]
#     switch which:
#       case 'to:'; to += lastLine[4]; break
#       case 'cc:': cc += lastLine[4]; break
#       case 'bcc': bcc += lastLine[5]; break


#———————————————————————————————————————— send message

  message = stripQuotes(message)
  #esponse = send_mail.send(settings, subject, to, bcc, message)
  response = send(settings, subject, to, [], bcc, message)
  return HttpResponse(response)


#:::::::::::::::::::::::::::::::::::::::: functions

#———————————————————————————————————————— stripQuotes(str)

def stripQuotes(str):
  str = re.sub('"', "''", str)
  str = re.sub("'", "’" , str)
  str = re.sub("`", "’" , str)
  return str

#———————————————————————————————————————— send(settings, subject, to, bcc, body)

# accepts subject, body, [to1, to2], [cc1, cc2], [bcc1, bcc2]
# abstract to a module when done

def send(settings, subject, to, cc, bcc, body):
# frm = settings.url + '<'+to+'>'
  email = EmailMessage('line120', 'World', to=['svijalove@hotmail.com','andy@svija.com'],bcc=['camrias@free.fr'])

  ht  = settings.mail_srv
  ht  = socket.gethostbyname(ht) # https://stackoverflow.com/questions/31663454/django-send-mail-through-gmail-very-slow
  pt  = settings.mail_port
  un  = settings.mail_id
  pw  = settings.mail_pass
  tls = settings.mail_tls

  connection = get_connection(host=ht,port=pt,username=un,password=pw,use_tls=tls)
  response   = ''

  try:
    connection.open()
    email.connection = connection
    email.send()
    connection.close()
  except SMTPException as e:
    response = e

  return response


#———————————————————————————————————————— fin
