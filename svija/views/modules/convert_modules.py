
#:::::::::::::::::::::::::::::::::::::::: views/modules/convert_modules.py

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

def convert_modules(modules, section_code, screen_code):

  out_modules = []

  for set in modules:
    mod = set.module
    if all([
      mod.enabled,
      str(mod.section)==section_code or str(mod.section)=='★',
      str(mod.screen)==screen_code or str(mod.screen)=='★',
    ]):
      mod.zindex = set.zindex
      out_modules.append(mod)

  return out_modules

#:::::::::::::::::::::::::::::::::::::::: fin

