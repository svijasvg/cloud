#———————————————————————————————————————— views/modules/get_page_scripts.py

#———————————————————————————————————————— notes
#
#   very similar:   get_page_scripts.py
#                   get_page_modules.py
#                   get_modules.py
#                   get_scripts.py
#
#
#   accepts a list of scripts , some inactive
#
#   returns a list of page objects
#   a page object contains css, headjs, bodyjs, svg, html, form etc.
#
#   when python is updated to at least 3.10, use pattern matching (like case/switch)
#   https://stackoverflow.com/questions/11479816/what-is-the-python-equivalent-for-a-case-switch-statement
#
#———————————————————————————————————————— imports

#rom modules.get_single_svg import *
from modules.get_script import *
from PageView import page_obj

#———————————————————————————————————————— def get_page_scripts(label, page_scripts):

# page.pagescript_set.filter(active=True).order_by('order')

def get_page_scripts(label, page_scripts):

  #comments
  hjc = hcc = bjc = svc = htc = fmc = ''

  final_list = []

#———————————————————————————————————————— iterate through scripts-linked-in-page

  for this_script_group in page_scripts:
    this_group = this_script_group.script

    hj = hc = bj = sv = ht = fm = ''

#———————————————————————————————————————— get SVG's

#   not used for scripts






#———————————————————————————————————————— deactivate from page?

    if this_group.active:

#———————————————————————————————————————— iterate through scripts

      for this_script in this_group.scriptscripts_set.all():
        if this_script.active:
    
          if this_script.type == 'head JS':
            hjc = '\n\n//———————————————————————————————————————— ' + label + '\n\n'
            hj += get_script('js', this_script.name, this_script.content)
    
          if this_script.type == 'CSS':
            hcc = '\n\n/*———————————————————————————————————————— ' + label + ' */\n\n'
            hc += get_script('css', this_script.name, this_script.content)
    
          if this_script.type == 'body JS':
            bjc = '\n\n//———————————————————————————————————————— ' + label + '\n\n'
            bj += get_script('js', this_script.name, this_script.content)
    
          if this_script.type == 'HTML':
            htc = '\n\n<!--—————————————————————————————————————— ' + label + ' -->\n\n'
            ht += get_script('html', this_script.name, this_script.content)
    
          if this_script.type == 'form':
            fmc = '\n\n<!--—————————————————————————————————————— ' + label + ' -->\n\n'
            fm += get_script('html', this_script.name, this_script.content)
  
#———————————————————————————————————————— append iteration results

      final_list.append(page_obj(hj, hc, bj, sv, ht, fm) )

#———————————————————————————————————————— prepare return

  comments = page_obj(hjc, hcc, bjc, svc, htc, fmc)
  final_list = [comments, *final_list]

  return final_list


#———————————————————————————————————————— fin
