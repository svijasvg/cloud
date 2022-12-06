#!/usr/bin/python
# -*- coding: UTF-8 -*-

#———————————————————————————————————————— modules/send_mail.py

# https://www.sitepoint.com/django-send-email/

# this is hard to debug — put it at end of MailView.py then
# copy back to this module when done

#———————————————————————————————————————— notes
#
#   see also:
#
#   go to /send to check if mail is being sent
#   correctly (views/SendView.py)
#
#   prints out message on fail, 1 on success
#   remember to check in "all mail" because mail
#   sent to myself is archived immediately
#
#   E1 failed whitelist address
#   E2 failed blacklist name
#   E3 failed blacklist body
#
#———————————————————————————————————————— imports

#mport sys
#mport os
#mport cgi
#mport re
#rom email.mime.text import MIMEText
#mport smtplib
#mport cgitb
#gitb.enable() # errors to browser

import socket
from smtplib import SMTPException
from django.core.mail import get_connection, EmailMessage


#———————————————————————————————————————— program

#ef send(settings, subject, to, bcc, body):
def send(settings, subject, body, frm, to, cc, bcc):

  if frm == '': frm = settings.mail_id

  email = EmailMessage(subject, body, from_email=frm, to=to, cc=cc, bcc=bcc)

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
