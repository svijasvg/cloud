#———————————————————————————————————————— views/modules/script_sets_dedupe.py

#———————————————————————————————————————— notes
#
#   accepts list of script sets and removes duplicates
#
#   duplicates happen when scripts are included both
#   via page settings and via script sets
#
#———————————————————————————————————————— imports

#rom modules.get_single_svg import *
from modules.get_script import *
from PageObject import page_obj

#———————————————————————————————————————— def script_sets_dedupe(scripts):

def script_sets_dedupe(scripts):

    out_scripts = []
    script_names = []

    for this_script_set in scripts:
        if script_names.count(this_script_set.name) == 0:
            script_names.append(this_script_set.name)
            out_scripts.append(this_script_set)

    return out_scripts

#———————————————————————————————————————— fin

