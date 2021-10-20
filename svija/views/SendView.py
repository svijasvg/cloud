#———————————————————————————————————————— SendView.py
#
# going to /fr/send will send a test email
# this is to eliminate confusion about
# where send failures come from
#
#———————————————————————————————————————— imports

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from svija.models import Settings, Language
from svija.views import PageView
from modules import send_mail

#———————————————————————————————————————— send mail


def SendView(request):
    if not request.user.is_superuser:
        response = PageView(request, 'en','missing',)
        response.status_code = 404
        return response

    settings = get_object_or_404(Settings, active=True)
    language_code = settings.language.code
    this_language = Language.objects.get(code=language_code)

    response = sendx(this_language)

    return HttpResponse(response)


#———————————————————————————————————————— imported from send_mail.py

#———————————————————————————————————————— imports

import sys
import os
import cgi
import re
import socket
from email.mime.text import MIMEText
import smtplib
from smtplib import SMTPException
from django.core.mail import get_connection, send_mail

#———————————————————————————————————————— errors to browser

import cgitb
cgitb.enable() 

#———————————————————————————————————————— function

def sendx(language):
    settings = get_object_or_404(Settings, active=True)

#———————————————————————————————————————— module paths

    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if not path in sys.path: sys.path.insert(1, path)
    del path

    fail = '' # send mail if not '' at end

    naim = 'test name' 
    addr = 'example@example.com' 
    body = 'email is working' 

    #———————————————————————————————————————— sendmail

    fail = mailit(settings, language, body)

    if fail == '': fail = 'mail sent successfully'
    return '<html><body><pre>' + str(fail)

#———————————————————————————————————————— function

def mailit(settings, language, body):

    fail = ''

    #—————————— site settings

    ht  = settings.mail_srv
    pt  = settings.mail_port
    un  = settings.mail_id
    pw  = settings.mail_pass
    tls = settings.mail_tls

    #—————————— language settings

    subject  = language.subject
    to       = language.email
    bcc      = language.bcc
#   default  = language.default
    no_email = language.no_email

    # https://stackoverflow.com/questions/31663454/django-send-mail-through-gmail-very-slow
    ht = socket.gethostbyname(ht)

    connection = get_connection(host=ht,port=pt,username=un,password=pw,use_tls=tls)

    frm = settings.url + '<'+to+'>'

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
        fail = e

    return fail

#———————————————————————————————————————— fin
