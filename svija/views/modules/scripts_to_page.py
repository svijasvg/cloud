#———————————————————————————————————————— views/modules/scripts_to_page.py

#———————————————————————————————————————— notes
#
#   very similar to modules/get_page_modules.py
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

from modules.get_script import *
from PageView import page_obj



#———————————————————————————————————————— def get_modules(label, all_scriptset_links, page_width, use_p3):

def scripts_to_page(label, all_scriptset_links):

  #comments
  hjc = hcc = bjc = svc = htc = fmc = ''

  comment_list = result_list = []

  # go through all scripts-linked-in-page
  for this_scriptset_link in all_scriptset_links:
    this_scriptset = this_scriptset_link.script

    hj = hc = bj = sv = ht = fm = ''

    if this_scriptset.active:

      #
      #
      #
      #
      # only in get_page_modules.py
      #
      #
      #

      for this_script in this_scriptset.scriptscripts_set.all():
        if this_script.active:
    
          if this_script.type == 'head JS':
            hj += get_script('js', this_script.name, this_script.content)
            hjc = '\n\n//———————————————————————————————————————— ' + label + '\n'
    
          if this_script.type == 'CSS':
            hc += get_script('css', this_script.name, this_script.content)
            hcc = '\n\n//———————————————————————————————————————— ' + label + '\n'
    
          if this_script.type == 'body JS':
            bj += get_script('js', this_script.name, this_script.content)
            bjc = '\n\n//———————————————————————————————————————— ' + label + '\n'
    
          if this_script.type == 'HTML':
            ht += get_script('html', this_script.name, this_script.content)
            htc = '\n\n//———————————————————————————————————————— ' + label + '\n'
    
          if this_script.type == 'form':
            fm += get_script('html', this_script.name, this_script.content)
            fmc = '\n\n//———————————————————————————————————————— ' + label + '\n'
  
    result_list.append(page_obj(hj, hc, bj, sv, ht, fm) )

  comment_list.append(page_obj(hjc, hcc, bjc, svc, htc, fmc))
  final_list = comment_list + result_list

  return final_list


#———————————————————————————————————————— fin
