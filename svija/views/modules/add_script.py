
#———————————————————————————————————————— add a script, returns string
# add a script (supplied or from file)
# with comment including it's name
# used in sort_modules

import os
import pathlib

def add_script(kind, name, content):

    # if it's in a file, we get that
    if len(content) < 100 and '\r' not in content and content.count('.') == 1:
        content = content.strip('/')
        source_path = os.path.abspath(os.path.dirname(__name__)) + '/sync/scripts/' + content
        path = pathlib.Path(source_path)
        if not path.exists():
            content = 'file not found: ' + content
        else:
            name = 'file: ' + name
            with open(source_path, 'r', encoding='utf-8') as f:
                content = f.read()

    # selective return, based on kind
    return {
        'html': '\n\n<!-- ' + name + ' -->\n' + content,
        'css' : '\n\n/* '   + name + ' */\n'  + content,
        'js'  : '\n\n// '   + name + '\n'     + content,
    }[kind]

