#———————————————————————————————————————— sort modules & scripts

# accepts a list of modules, some inactive
# a module has exactly 1 svg filename, and it can be empty

from modules.svg_cleaner import *
from modules.get_single_svg import *
from modules.add_script import *

def sort_modules(all_modules, source_dir, specified_width, use_p3):

    head_css = head_js = body_js = svg = html = form = ''

    for this_module in (obj.module for obj in all_modules if obj.active==True):

        s, c = get_single_svg(this_module, source_dir, specified_width, use_p3)
        svg += s
        head_css += c

        for this_script in this_module.modulescripts_set.all():
            if this_script.active:

                if this_script.type == 'CSS':
                    head_css += add_script('css', this_script.name, this_script.content)

                if this_script.type == 'head JS':
                    head_js += add_script('js', this_script.name, this_script.content)

                if this_script.type == 'body JS':
                    body_js += add_script('js', this_script.name, this_script.content)

                if this_script.type == 'HTML':
                    html += add_script('html', this_script.name, this_script.content)

                if this_script.type == 'form':
                    form += add_script('html', this_script.name, this_script.content)

    return head_css, head_js, body_js, svg, html, form
