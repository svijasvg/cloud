#———————————————————————————————————————— views/modules/convert_scripts.py

#———————————————————————————————————————— notes
#
#   accepts list of PageScripts
#   returns a list of Script Objects
#
#———————————————————————————————————————— imports

#rom modules.get_single_svg import *
from modules.get_script import *
from PageObject import page_obj

#———————————————————————————————————————— def convert_scripts(scripts):

def convert_script_sets(scripts):

  out_scripts = []

  for this_script_set in scripts:
    out_scripts.append(this_script_set.script)

  return out_scripts

#———————————————————————————————————————— fin
