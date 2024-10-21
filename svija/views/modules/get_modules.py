#———————————————————————————————————————— views/modules/get_all_modules.py

#———————————————————————————————————————— notes
#
#   accepts a list of modules, all enabled
#   can be wrong section/screen if user included it wrongly
#   a module has exactly 1 svg filename, and it can be empty
#
#———————————————————————————————————————— imports

from modules.get_single_svg import *
from modules.get_script import *
from PageView import page_obj

#———————————————————————————————————————— def get_all_modules(label, all_modules, section_code, screen_code, page, page_width, use_p3):

# page.pagemodule_set.filter(enabled=True).order_by('zindex')

def get_modules(label, all_modules, section_code, screen_code, page, page_width, use_p3):

  #comments
  hjc = hcc = bjc = svc = htc = fmc = ''

  final_list = []

#———————————————————————————————————————— NEED TO SORT MODULES BY Z INDEX

  all_modules.sort(key = lambda x: x.zindex)

#———————————————————————————————————————— iterate through modules-linked-in-page

  for this_module in all_modules:

    hj = hc = bj = sv = ht = fm = ''

    if (this_module.section.code == section_code
    and this_module.screen.code  == screen_code):

#———————————————————————————————————————— get SVG's

      svc = '\n\n<!--———————————————————————————————————————— ' + label + ' -->\n\n'
  
      sv, hc, rien = get_single_svg(this_module, screen_code, page_width, use_p3, False, '')

#———————————————————————————————————————— iterate through scripts

      enabled_scripts = list(this_module.modulescript_set.filter(enabled=True))

      for this_script in enabled_scripts:
  
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
