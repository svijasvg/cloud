#———————————————————————————————————————— views/modules/contains_form.py

from PageView import page_obj

def contains_form(content_blocks):
    form = ''.join([ i['form'] for i in content_blocks] )
    if form != '': return True
    else: return False
