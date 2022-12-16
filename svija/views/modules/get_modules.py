#———————————————————————————————————————— views/modules/get_modules.py

#———————————————————————————————————————— notes
#
#   very similar:   get_modules.py
#                   get_page_modules.py
#                   get_page_scripts.py
#                   get_scripts.py
#
#   accepts a list of modules, all enabled
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
from PageObject import page_obj

#———————————————————————————————————————— def get_modules(label, all_modules, page_width, use_p3):

# Module.objects.filter(Q(section__code=section_code) & Q(screen__code=screen_code) & Q(enabled=True) & Q(always=True)).order_by('order')

def get_modules(label, all_modules, screen_code, page, page_width, use_p3):

  #comments
  hjc = hcc = bjc = svc = htc = fmc = ''

  final_list = []

#———————————————————————————————————————— iterate through modules

  for this_group in all_modules:


    hj = hc = bj = sv = ht = fm = ''

#———————————————————————————————————————— get SVG's

    # returns svg and css
    sv, hc, rien = get_single_svg(this_group, screen_code, page_width, use_p3)




#———————————————————————————————————————— deactivate from page?

#   not called through page

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
