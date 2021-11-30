#———————————————————————————————————————— views/modules/scripts_to_page.py
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

#———————————————————————————————————————— def get_modules(label, all_linked_script_sets, page_width, use_p3):

def scripts_to_page(label, all_linked_script_sets):

  #comments
  hjc = hcc = bjc = svc = htc = fmc = ''

  comment_list = script_list = []

  # go through all scripts-linked-in-page
  for this_linked_script_set in all_linked_script_sets:
    this_script_set = this_linked_script_set.script


# need to get all scripts and set correct order before
# iterating through them.

    hj = hc = bj = sv = ht = fm = ''

    if this_script_set.active:
      for this_script in this_script_set.scriptscripts_set.all():

        if this_script.active:
    
          if this_script.type == 'head JS':
            hj += get_script('js', this_script.name, this_script.content)
            hjc = '\n\n//———————————————————————————————————————— head js' + label + '\n'
    
          if this_script.type == 'CSS':
            hc += get_script('css', this_script.name, this_script.content)
            hcc = '\n\n//———————————————————————————————————————— css ' + label + '\n'
    
          if this_script.type == 'body JS':
            bj += get_script('js', this_script.name, this_script.content)
            bjc = '\n\n//———————————————————————————————————————— body js ' + label + '\n'
    
          if this_script.type == 'HTML':
            ht += get_script('html', this_script.name, this_script.content)
            htc = '\n\n//———————————————————————————————————————— html ' + label + '\n'
    
          if this_script.type == 'form':
            fm += get_script('html', this_script.name, this_script.content)
            fmc = '\n\n//———————————————————————————————————————— form ' + label + '\n'
  
    script_list.append(page_obj(hj, hc, bj, sv, ht, fm) )

  comment_list.append(page_obj(hjc, hcc, bjc, '', htc, fmc))
  final_list = comment_list + script_list

  return final_list


#———————————————————————————————————————— fin
