#!/usr/bin/python
# -*- coding: UTF-8 -*-

#---------------------------------------- modules/send_mail.py
#
#        prints out 0 on fail, 1 on success
#        remember to check in "all mail" because mail
#        sent to myself is archived immediately
#
#----------------------------------------- imports

import sys
import os
import cgi
import re
from email.mime.text import MIMEText
import smtplib
from django.core.mail import get_connection, send_mail

import cgitb
cgitb.enable() # errors to browser

#---------------------------------------- function

def send(settings, language, request, ua):

#---------------------------------------- accept dangerous mail?

    accept_failed = True;
    sendmail_location = "/usr/sbin/sendmail"

#---------------------------------------- module paths

    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if not path in sys.path: sys.path.insert(1, path)
    del path

    fail = 0 # send mail if 0, fail if 1

#----------------------------------------- configuration

    to       = language.email
    bcc      = language.bcc
    default  = language.default
    no_email = language.no_email
    subject  = language.subject + ' ' + settings.url

#----------------------------------------- get form data

    naim = str(request.get('name'))
    addr = request.get('email').lower()
    body = request.get('message')

#----------------------------------------- validate email / telephone

    whitelisttel  = re.compile("^\+?[0-9,\-,\.,' ',\(,\)]+$") # https://regex101.com
    whitelistmail = re.compile("[a-z,0-9,\.,_,-]+\@[a-z,0-9,\.,-]+\.[a-z]+")
    
    blacklist = ".*[\\|\^|\$|\||\*|\+|\[|\{|<|>]+.*"
    
    if not whitelisttel.match(addr) and not whitelistmail.match(addr):
        fail = 1; body = 'ADDRESS FAILED WHITELIST: ' + body
    
    if re.match(blacklist, naim):
        fail = 1; body = 'NAME FAILED BLACKLIST: ' + body
    
    if re.match(blacklist, body):
        fail = 1; body = 'MESSAGE FAILED BLACKLIST: ' + body
    
    #----------------------------------------- if fail get out
    #----------------------------------------- disabled for debugging
    
    if fail == 1 and accept_failed == False:
        return 0
    
    #----------------------------------------- content is ok, we can send the mail
    
    #----------------------------------------- make legible tel number
    
    if addr.find('@') < 0: # tel supplied but no name
        addr = re.sub('\(',  '[', addr) # google hides 
        addr = re.sub('\)',  ']', addr) # numbers in parentheses
        addr = re.sub('-',  ' ', addr)
        addr = re.sub('\.', ' ', addr)
    
    #----------------------------------------- prepare parts of email address
    
    if naim != '': name = naim; # name supplied
    
    elif addr.find('@') > 0: # only email given 
        name, crap = addr.split('@')
        name = re.sub("_", " ", name)
        name = re.sub("\.", " ", name)
        name = name.title() # http://www.codetable.net/Group/miscellaneous-symbols
    
    else:
        name = addr # only phone number given
        addr = no_email
    
    #----------------------------------------- from info for body of message
    
    sig = language.mail_frm + ' ' + name + ' <' + addr + '>\n\n'
    
    #----------------------------------------- visible "from" address
    
    if addr.find('@') < 0: addr = default
    
    #----------------------------------------- convert quote to harmless equivalent
    
    body = re.sub('"', "''", body) # double quotes to single quotes
    body = re.sub("'", "’", body)  # single quotes to smart quotes
    body = '\n' + body
    
    #----------------------------------------- add browser info to mail
    
    body = sig + body
    
    s = ua.split(') ')
    sep = ')\n'
    body += "\n\n----------------------------------------\n" +sep.join(s)
    
    #----------------------------------------- sendmail

    ht = settings.mail_srv
    pt = settings.mail_port
    un = settings.mail_id
    pw = settings.mail_pass
    tls = settings.mail_tls
    connection = get_connection(host=ht,port=pt,username=un,password=pw,use_tls=tls)

    send_mail(
        subject,
        body,
        name + ' <' + addr + '>',
        [to, bcc,],
        fail_silently=False,
        connection=connection,
    )

    #----------------------------------------- success
    
    if fail == 1: return 0
    else: return 1
    
    #----------------------------------------- fin
