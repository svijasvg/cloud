#!/usr/bin/python
# -*- coding: UTF-8 -*-

#———————————————————————————————————————— modules/send_mail.py
#
#   called by views.MailView
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

def send(settings, language, request, ua):

#———————————————————————————————————————— accept dangerous mail?

    accept_failed = True;

#———————————————————————————————————————— module paths

    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if not path in sys.path: sys.path.insert(1, path)
    del path

    fail = '' # send mail if not '' at end

#———————————————————————————————————————— get form data

    naim = str(request.get('name'))
    addr = request.get('email').lower()
    body = request.get('message')

#———————————————————————————————————————— validate email / telephone

    whitelisttel  = re.compile("^\+?[0-9,\-,\.,' ',\(,\)]+$") # https://regex101.com
    whitelistmail = re.compile("[a-z,0-9,\.,_,-]+\@[a-z,0-9,\.,-]+\.[a-z]+")

    blacklist = ".*[\\|\^|\$|\||\*|\+|\[|\{|<|>]+.*"

    if not whitelisttel.match(addr) and not whitelistmail.match(addr):
        fail += ' E1'; body = 'ADDRESS FAILED WHITELIST. ' + body

    if re.match(blacklist, naim):
        fail += ' E2'; body = 'NAME FAILED BLACKLIST. ' + body

    if re.match(blacklist, body):
        fail += ' E3'; body = 'MESSAGE FAILED BLACKLIST. ' + body

    #———————————————————————————————————————— if fail get out
    #———————————————————————————————————————— disabled for debugging

    if fail != '' and accept_failed == False:
        return failed

    #———————————————————————————————————————— content is ok, we can send the mail

    #———————————————————————————————————————— make legible tel number

    if addr.find('@') < 0: # tel supplied but no name
        addr = re.sub('\(',  '[', addr) # google hides
        addr = re.sub('\)',  ']', addr) # numbers in parentheses
        addr = re.sub('-',  ' ', addr)
        addr = re.sub('\.', ' ', addr)

    #———————————————————————————————————————— prepare parts of email address

    if naim != '': name = naim; # name supplied

    elif addr.find('@') > 0: # only email given
        name, crap = addr.split('@')
        name = re.sub("_", " ", name)
        name = re.sub("\.", " ", name)
        name = name.title() # http://www.codetable.net/Group/miscellaneous-symbols

    else:
        name = addr # only phone number given
        addr = no_email

    #———————————————————————————————————————— from info for body of message

    sig = language.mail_frm + ' ' + name + ' <' + addr + '>\n\n'

    #———————————————————————————————————————— visible "from" address

    if addr.find('@') < 0: addr = default
    frm = settings.url+ ' <' + addr + '>'

    #———————————————————————————————————————— convert quote to harmless equivalent

    body = re.sub('"', "''", body) # double quotes to single quotes
    body = re.sub("'", "’", body)  # single quotes to smart quotes
    body = '\n' + body

    #———————————————————————————————————————— add browser info to mail

    body = sig + body

    s = ua.split(') ')
    sep = ')\n'
    body += "\n\n————————————————————————————————————————\n" +sep.join(s)

#———————————————————————————————————————— configuration

    to       = language.email
    bcc      = language.bcc
    default  = language.default
    no_email = language.no_email
    subject  = language.subject + ' ' + settings.url

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
            fail_silently=False,
            connection=connection,
        )
    except SMTPException as e:
        fail = e

    #———————————————————————————————————————— success

    if fail == '': return 1
    else: return fail

#———————————————————————————————————————— fin
