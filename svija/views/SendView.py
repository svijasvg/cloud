#———————————————————————————————————————— SendView.py
# /fr/mail sends mail (needs language code)

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from svija.models import Prefix, Settings
from svija.views import PageView

#———————————————————————————————————————— send mail

from modules import send_mail

def SendView(request, lng):
    if not request.user.is_superuser:
        response = PageView(request, 'en','missing',)
        response.status_code = 404
        return response

    pfix = get_object_or_404(Prefix, path=lng)
    lng = pfix.language

    response = sendx(lng)

    return HttpResponse(response)

#———————————————————————————————————————— imported from send_mail.py

import sys
import os
import cgi
import re
import socket
from email.mime.text import MIMEText
import smtplib
from smtplib import SMTPException
from django.core.mail import get_connection, send_mail

import cgitb
cgitb.enable() # errors to browser

#———————————————————————————————————————— function

def sendx(language):
    settings = get_object_or_404(Settings, active=True)


#———————————————————————————————————————— module paths

    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if not path in sys.path: sys.path.insert(1, path)
    del path

    fail = '' # send mail if not '' at end

    #———————————————————————————————————————— configuration

    naim = 'test name' 
    addr = 'example@example.com' 
    body = 'email is working' 
    frm = addr

    to       = language.email
    bcc      = language.bcc
    default  = language.default
    no_email = language.no_email
    subject  = language.subject

    #———————————————————————————————————————— sendmail

    ht = settings.mail_srv
    pt = settings.mail_port
    un = settings.mail_id
    pw = settings.mail_pass
    tls = settings.mail_tls

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
        fail = e

    if fail == '': fail = 'mail sent successfully'
    return '<html><body><pre>' + str(fail)

    #———————————————————————————————————————— fin
