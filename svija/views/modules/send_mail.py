#!/usr/bin/python
# -*- coding: UTF-8 -*-

#———————————————————————————————————————— modules/send_mail.py

# https://www.sitepoint.com/django-send-email/

#———————————————————————————————————————— notes
#
#   see also:
#
#   got to /send to check if mail is being sent
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
from django.core.mail import get_connection, send_mail


#———————————————————————————————————————— program

def send(settings, subject, to, bcc, body):

    response = ''

    #—————————— site settings

    ht  = settings.mail_srv
    pt  = settings.mail_port
    un  = settings.mail_id
    pw  = settings.mail_pass
    tls = settings.mail_tls
    frm = settings.url + '<'+to+'>'

    # https://stackoverflow.com/questions/31663454/django-send-mail-through-gmail-very-slow
    ht = socket.gethostbyname(ht)

    connection = get_connection(host=ht,port=pt,username=un,password=pw,use_tls=tls)

    try:
        send_mail(
            subject,
            body,
            frm,
            [to, bcc,],
            fail_silently=True,
            connection=connection,
        )
    except SMTPException as e:
        response = e

    return response


#———————————————————————————————————————— fin
