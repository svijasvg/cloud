#———————————————————————————————————————— views/modules/get_modules.py

# accepts a list of modules, some inactive
# a module has exactly 1 svg filename, and it can be empty

from modules.svg_cleaner import *
from modules.get_single_svg import *
from modules.add_script import *
from PageView import page_obj

def get_modules(label, all_modules, source_dir, specified_width, use_p3):

    head_css = head_js = body_js = svgs = html = form = ''

    module_list = []

    head_js += '\n\n//———————————————————————————————————————— ' + label + '\n\n'
    body_js += '\n\n//———————————————————————————————————————— ' + label + '\n\n'

    for this_module in (obj.module for obj in all_modules if obj.active==True):

#       self.head_js    = head_js
#       self.css        = css
#       self.body_js    = body_js
#       self.svgs       = svgs
#       self.html       = html
#       self.form       = form

        xh = xc = xb = xs = xh = xm = ''

        s, c = get_single_svg(this_module, source_dir, specified_width, use_p3)
        svgs += s
        head_css += c

        xs = s
        xc = c

        for this_script in this_module.modulescripts_set.all():
            if this_script.active:

                if this_script.type == 'CSS':
                    head_css += add_script('css', this_script.name, this_script.content)
                    xc += add_script('css', this_script.name, this_script.content)

                if this_script.type == 'head JS':
                    head_js += add_script('js', this_script.name, this_script.content)
                    xh += add_script('js', this_script.name, this_script.content)

                if this_script.type == 'body JS':
                    body_js += add_script('js', this_script.name, this_script.content)
                    xb += add_script('js', this_script.name, this_script.content)

                if this_script.type == 'HTML':
                    html += add_script('html', this_script.name, this_script.content)
                    xh += add_script('html', this_script.name, this_script.content)

                if this_script.type == 'form':
                    form += add_script('html', this_script.name, this_script.content)
                    xm += add_script('html', this_script.name, this_script.content)

        module_list.append(page_obj(xh, xc, xb, xs, xh, xm) )

    return module_list
