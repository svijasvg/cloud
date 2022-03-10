#———————————————————————————————————————— views/modules/get_modules.py

#———————————————————————————————————————— notes
#
#   very similar to modules/scripts_to_page.py
#
#   accepts a list of modules, some inactive
#   a module has exactly 1 svg filename, and it can be empty
#
#
#
#
#
#
#———————————————————————————————————————— imports

from modules.svg_cleaner import *
from modules.get_single_svg import *
from modules.get_script import *
from PageView import page_obj

#———————————————————————————————————————— def get_page_modules(label, all_module_links, language_code, screen_code, page, page_width, use_p3):

def get_page_modules(label, all_module_links, language_code, screen_code, page, page_width, use_p3):

  #comments
  hjc = hcc = bjc = svc = htc = fmc = ''

  final_list = result_list = []

#———————————————————————————————————————— go through all modules-linked-in-page

  for this_module_link in all_module_links:

    this_module = this_module_link.module

    hj = hc = bj = sv = ht = fm = ''

#———————————————————————————————————————— if active

    if (this_module.always
    and this_module.language.code == language_code
    and this_module.screen.code   == screen_code):
  
      s, c = get_single_svg(this_module, screen_code, page_width, use_p3)

      sv  = s
      hc  = c
      svc = '\n\n<!--———————————————————————————————————————— ' + label + ' -->\n\n'
  
#———————————————————————————————————————— iterate through scripts

      for this_script in this_module.modulescript_set.all():
        if this_script.active:
    
          if this_script.type == 'head JS':
            hj += get_script('js', this_script.name, this_script.content)
            hjc = '\n\n//———————————————————————————————————————— ' + label + '\n\n'
    
          if this_script.type == 'CSS':
            hc += get_script('css', this_script.name, this_script.content)
            hcc = '\n\n/*———————————————————————————————————————— ' + label + ' */\n\n'
    
          if this_script.type == 'body JS':
            bj += get_script('js', this_script.name, this_script.content)
            bjc = '\n\n//———————————————————————————————————————— ' + label + '\n\n'
    
          if this_script.type == 'HTML':
            ht += get_script('html', this_script.name, this_script.content)
            htc = '\n\n<!--—————————————————————————————————————— ' + label + ' -->\n\n'
    
          if this_script.type == 'form':
            fm += get_script('html', this_script.name, this_script.content)
            fmc = '\n\n<!--—————————————————————————————————————— ' + label + ' -->\n\n'
  
#———————————————————————————————————————— append iteration results

      result_list.append(page_obj(hj, hc, bj, sv, ht, fm) )

#———————————————————————————————————————— prepare return

  final_list = [page_obj(hjc, hcc, bjc, svc, htc, fmc)]
  final_list.extend(result_list)

  return final_list


#———————————————————————————————————————— fin
