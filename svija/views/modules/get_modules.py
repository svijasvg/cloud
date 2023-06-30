#———————————————————————————————————————— views/modules/get_modules.py

#———————————————————————————————————————— notes
#
#   accepts a list of modules, all enabled & always include
#   and with correct screen code & section
#
#———————————————————————————————————————— imports

from modules.get_single_svg import *
from modules.get_script import *
from PageObject import page_obj

#———————————————————————————————————————— def get_modules(label, all_modules, page_width, use_p3):

# Module.objects.filter(Q(section__code=section_code) & Q(screen__code=screen_code) & Q(enabled=True) & Q(always=True)).order_by('order')

def get_modules(all_modules):

  final_list = []

#———————————————————————————————————————— iterate through scripts

  for this_group in all_modules:
    final_list.append(this_group)

  return final_list

#———————————————————————————————————————— fin
