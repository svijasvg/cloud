#———————————————————————————————————————— views/modules/get_modules.py

# accepts a list of modules, some inactive
# a module has exactly 1 svg filename, and it can be empty

from modules.svg_cleaner import *
from modules.get_single_svg import *
from modules.get_script import *
from PageView import page_obj

def get_modules(label, all_modules, page_width, use_p3):

    head_css = head_js = body_js = svgs = html = form = ''

    module_list = []

    head_js += '\n\n//———————————————————————————————————————— ' + label + '\n\n'
    body_js += '\n\n//———————————————————————————————————————— ' + label + '\n\n'

    for this_module in all_modules:

        hj = hc = bj = sv = ht = fm = ''

        s, c = get_single_svg(this_module, page_width, use_p3)
        svgs     += s
        head_css += c

        sv = s
        hc = c

        if hasattr(this_module, 'modulescripts'):
            for this_script in this_module.modulescripts_set.all():
                if this_script.active:
    
                    if this_script.type == 'head JS':
                        head_js += get_script('js', this_script.name, this_script.content)
                        hj += get_script('js', this_script.name, this_script.content)
    
                    if this_script.type == 'CSS':
                        head_css += get_script('css', this_script.name, this_script.content)
                        hc += get_script('css', this_script.name, this_script.content)
    
                    if this_script.type == 'body JS':
                        body_js += get_script('js', this_script.name, this_script.content)
                        bj += get_script('js', this_script.name, this_script.content)
    
                    # SVG handled outside of loop
    
                    if this_script.type == 'HTML':
                        html += get_script('html', this_script.name, this_script.content)
                        ht += get_script('html', this_script.name, this_script.content)
    
                    if this_script.type == 'form':
                        form += get_script('html', this_script.name, this_script.content)
                        fm += get_script('html', this_script.name, this_script.content)
    
        module_list.append(page_obj(hj, hc, bj, sv, ht, fm) )

    return module_list
