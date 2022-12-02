#———————————————————————————————————————— views/modules/get_page_modules.py

#———————————————————————————————————————— notes
#
#   very similar:   get_modules.py
#                   get_page_modules.py
#                   get_page_scripts.py
#                   get_scripts.py
#
#   accepts a list of modules, some disabled
#   a module has exactly 1 svg filename, and it can be empty
#
#
#
#
#
#
#
#———————————————————————————————————————— imports

from modules.get_single_svg import *
from modules.get_script import *
from PageView import page_obj

#———————————————————————————————————————— def get_page_modules(label, page_modules, section_code, screen_code, page, page_width, use_p3):

# page.pagemodule_set.filter(enabled=True).order_by('zindex')

def get_page_modules(label, page_modules, section_code, screen_code, page, page_width, use_p3):

  #comments
  hjc = hcc = bjc = svc = htc = fmc = ''

  final_list = []

#———————————————————————————————————————— iterate through modules-linked-in-page

  for this_module in page_modules:
    this_group = this_module.module

    hj = hc = bj = sv = ht = fm = ''

#———————————————————————————————————————— get SVG's

    if (this_group.section.code == section_code
    and this_group.screen.code   == screen_code):
      svc = '\n\n<!--———————————————————————————————————————— ' + label + ' -->\n\n'
  
      sv, hc = get_single_svg(this_group, screen_code, page_width, use_p3)

#———————————————————————————————————————— deactivate from page?

      if this_group.enabled:

#———————————————————————————————————————— iterate through scripts

        for this_script in this_group.modulescript_set.all():
          if this_script.enabled:
    
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
