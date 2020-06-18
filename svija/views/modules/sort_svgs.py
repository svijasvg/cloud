#———————————————————————————————————————— sort SVG's & scripts
# line 431, 495:

from modules import svg_cleaner

def sort_svgs_scripts(flag, ordering, source_dir, all_svgs, specified_width, use_p3):

    head_css = head_js = body_js = svg = ''

    if len(ordering) > 0:
        all_svgs = []

    for dooby in ordering:
        if dooby.active:
            all_svgs.append(dooby.module)

#    some_svgs = {k:all_svgs[k] for k in ('active') if k}
    
    head_css = head_js = body_js = svg = ''
    for this_svg in all_svgs: #WHERE ACTIVE == TRUE, ORDER BY LOAD_ORDER
        if this_svg.active:
            if this_svg.filename != '':

                #—————— check if svg exists
                temp_source = os.path.abspath(os.path.dirname(__name__)) + '/' + source_dir + '/' + this_svg.filename
                path = pathlib.Path(temp_source)
                if not path.exists():
                    svg = '<!-- missing svg: {} -->'.format(this_svg.filename)

                else:
                    svg_ID, svg_width, svg_height, svg_content = svg_cleaner.clean(temp_source, this_svg.filename, use_p3)
    
                    if svg_width > specified_width:
                        page_ratio = svg_height/svg_width
                        svg_width = specified_width
                        svg_height = round(specified_width * page_ratio)

                    rem_width = svg_width/10
                    rem_height = svg_height/10
        
                    css_dims = '#' + svg_ID + '{ width:' + str(rem_width) + 'rem; height:' + str(rem_height) + 'rem; }'
                    head_css += '\n\n' + css_dims
                    svg += '\n' + svg_content

            try:
                all_scripts = this_svg.modulescripts_set.all() # IN ORDER
                for this_script in all_scripts:
                    if this_script.type == 'CSS' and this_script.active == True:
                        head_css += add_script('css', this_script.name, this_script.content)
                    if this_script.type == 'head JS' and this_script.active == True:
                        head_js += add_script('js', this_script.name, this_script.content)
                    if this_script.type == 'body JS' and this_script.active == True:
                        body_js += add_script('js', this_script.name, this_script.content)
            except:
                rien = 0

    results = {
        'head_css': head_css,
        'head_js' : head_js,
        'body_js' : body_js,
        'svg'     : svg,
    }
    return results


