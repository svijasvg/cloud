#———————————————————————————————————————— views/modules/get_scripts.py

#———————————————————————————————————————— notes
#
#   very similar:   get_page_scripts.py
#                   get_page_modules.py
#                   get_modules.py
#                   get_scripts.py
#
#
#   accepts a list of scripts, all active & "always include"
#
#
#
#
#
#
#
#———————————————————————————————————————— imports

#rom modules.get_single_svg import *
from modules.get_script import *
from PageView import page_obj

#———————————————————————————————————————— def get_scripts(label, all_scripts, page_width, use_p3):

# Script.objects.filter(Q(active=True) & Q(always=True))

def get_scripts(label, all_scripts):

  #comments
  hjc = hcc = bjc = svc = htc = fmc = ''

  final_list = []

#———————————————————————————————————————— iterate through scripts

  for this_group in all_scripts:


    hj = hc = bj = sv = ht = fm = ''

#———————————————————————————————————————— get SVG's

#   not used for scripts






#———————————————————————————————————————— deactivate from page?

#   not called through page

#———————————————————————————————————————— iterate through scripts

    for this_script in this_group.scriptscripts_set.all():
      if this_script.active:
  
        if this_script.type == 'head JS':
          hjc += get_script('js', this_script.name, this_script.content)
          hj += get_script('js', this_script.name, this_script.content)
   
        if this_script.type == 'CSS':
          hcc += get_script('css', this_script.name, this_script.content)
          hc += get_script('css', this_script.name, this_script.content)
   
        if this_script.type == 'body JS':
          bjc += get_script('js', this_script.name, this_script.content)
          bj += get_script('js', this_script.name, this_script.content)
   
        if this_script.type == 'HTML':
          htc += get_script('html', this_script.name, this_script.content)
          ht += get_script('html', this_script.name, this_script.content)
   
        if this_script.type == 'form':
          fmc += get_script('html', this_script.name, this_script.content)
          fm += get_script('html', this_script.name, this_script.content)
  
#———————————————————————————————————————— append iteration results

      final_list.append(page_obj(hj, hc, bj, sv, ht, fm) )

#———————————————————————————————————————— prepare return

  comments = page_obj(hjc, hcc, bjc, svc, htc, fmc)
  final_list = [comments, *final_list]

  return final_list


#———————————————————————————————————————— fin
