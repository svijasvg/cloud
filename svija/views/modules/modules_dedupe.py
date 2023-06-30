#———————————————————————————————————————— views/modules/modules_dedupe.py

#———————————————————————————————————————— notes
#
#   accepts list of module and removes duplicates
#
#   duplicates happen when modules are included both
#   via page settings and via modules
#
#———————————————————————————————————————— imports

#rom modules.get_single_svg import *
#rom modules.get_module import *
#rom PageObject import page_obj

#———————————————————————————————————————— def modules_dedupe(modules):

def modules_dedupe(modules):

  out_modules = []
  module_names = []

  for this_module in modules:
    if module_names.count(this_module.name) == 0:
      module_names.append(this_module.name)
      out_modules.append(this_module)

  return out_modules

#———————————————————————————————————————— fin
