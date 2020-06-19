    #———————————————————————————————————————— form-oriented language variables

    # added down below if there is a form
def generate_form_js(language):

    form_js = '\n//———————————————————————————————————————— mail form\n\n'

    form_js += 'var name_init = "'      + language.form_name       + '";\n'
    form_js += 'var address_init = "'   + language.form_email      + '";\n'
    form_js += 'var status_init = "'    + language.form_status     + '";\n'
    form_js += 'var send_init = "'      + language.form_send       + '";\n'
    form_js += 'var mess_sending = "'   + language.form_sending    + '";\n'
    form_js += 'var mess_received = "'  + language.form_rcvd       + '";\n'
    form_js += 'var alert_received = "' + language.form_alert_rcvd + '";\n'
    form_js += 'var alert_failed = "'   + language.form_alert_fail  + '";\n'

#var address_failed = 'cxoxnxtxaxcxtx@xoxzxaxkxex.xcxom';

#var alert_failed   = 'Your message could not be sent.\n\nPlease send it directly to '
#                   + address_failed.replace(/x/g,'');

    alert_char  = 'x' # should be calculated
    alert_email = alert_char.join(list(language.email))

    form_js += 'var alert_email  = "'   + alert_email + '";\n'
    form_js += 'var alert_char   = "'   + alert_char  + '";\n'
    form_js += '\n//———————————————————————————————————————— /mail form\n\n'

    return form_js
