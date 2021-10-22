#———————————————————————————————————————— form-oriented language variables

# added down below if there is a form

#ef generate_form_js(language):

#ef generate_form_js(core_content, language):

#   if core_content['form'] == '':
#       return core_content

#———————————————————————————————————————— generate_form_js(language):

def generate_form_js(language):

    form_js = '\n//———————————————————————————————————————— mail form\n\n'

    form_js += 'var form_dest = "'       + scape(language.email          ) + '";\n'
    form_js += 'var form_subject = "'    + scape(language.subject        ) + '";\n'
    form_js += 'var form_fromlable = "'  + scape(language.mail_frm       ) + '";\n'
    
    form_js += 'var name_init = "'       + scape(language.form_name      ) + '";\n'
    form_js += 'var business_init = "'   + scape(language.form_business  ) + '";\n'
    form_js += 'var address_init = "'    + scape(language.form_email     ) + '";\n'
    form_js += 'var message_init = "'    + scape(language.form_message   ) + '";\n'
    form_js += 'var send_init = "'       + scape(language.form_send      ) + '";\n'

    form_js += 'var status_init = "'     + scape(language.form_status    ) + '";\n'
    form_js += 'var status_sending = "'  + scape(language.form_sending   ) + '";\n'
    form_js += 'var status_failed = "'   + scape(language.form_alert_fail) + '";\n'
    form_js += 'var status_received = "' + scape(language.form_rcvd      ) + '";\n'
    form_js += 'var alert_received = "'  + scape(language.form_alert_rcvd) + '";\n'

#var address_failed = 'cxoxnxtxaxcxtx@xoxzxaxkxex.xcxom';

#var alert_failed   = 'Your message could not be sent.\n\nPlease send it directly to '
#                   + address_failed.replace(/x/g,'');

    alert_char  = 'x' # should be calculated
    alert_email = alert_char.join(list(language.email))

    form_js += 'var alert_email  = "'   + alert_email + '";\n'
    form_js += 'var alert_char   = "'   + alert_char  + '";\n'
    form_js += '\n//———————————————————————————————————————— /mail form\n\n'

#   core_content['body_js'] += form_js
#   return core_content

    return form_js

#———————————————————————————————————————— function

def scape(str):

# only double quotes are escaped because only double quotes
# are used to assign the values to a variable

  str = str.replace('"', '\\"')
# str = str.replace("'", "\\'")
  return str

