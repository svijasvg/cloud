#———————————————————————————————————————— views/modules/convert_modules.py

#———————————————————————————————————————— notes
#
#   accepts list of PageModule
#   returns a list of Module Objects
#
#———————————————————————————————————————— imports

#rom modules.get_single_svg import *
#rom modules.get_module import * # CAUSES CRASH
#rom PageObject import page_obj

#———————————————————————————————————————— def convert_modules(modules):

def convert_modules(modules):

  out_modules = []

  for this_module_set in modules:
    if this_module_set.module.enabled:
      out_modules.append(this_module_set.module)

  return out_modules

#———————————————————————————————————————— fin
