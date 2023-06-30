#———————————————————————————————————————— views/modules/get_scripts.py

#———————————————————————————————————————— notes
#
#   accepts a list of scripts, all enabled & "always include"
#
#———————————————————————————————————————— imports

#rom modules.get_single_svg import *
from modules.get_script import *
from PageObject import page_obj

#———————————————————————————————————————— def get_scripts(label, all_scripts, page_width, use_p3):

# Script.objects.filter(Q(enabled=True) & Q(always=True))

def get_scripts(all_scripts):

  final_list = []

#———————————————————————————————————————— iterate through scripts

  for this_group in all_scripts:

    for this_script in this_group.scriptscripts_set.all():
      if this_script.enabled:
        final_list.append(this_script)

  return final_list


#———————————————————————————————————————— fin
