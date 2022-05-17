#———————————————————————————————————————— add accessbility, returns string
#
# add accessibilithy text (supplied or from file)

#———————————————————————————————————————— import

import os
import pathlib
import re

#———————————————————————————————————————— get_accessibility(content):

def get_accessibility(content):

    # https://regex101.com
    # matches a-z   0-9   \s   .   _   +   -   &  .txt or .html
    filename = re.compile("^<p>[a-z,0-9,\s,\.,_,+,\-,&]+\.(txt|html)</p>$", re.I) 

    if filename.match(content):
        content = content[3:-4] # remove <p> tags
        sub_path = '/sync/Svija/Accessibility/' + content
        source_path = os.path.abspath(os.path.dirname(__name__)) + sub_path 
        path = pathlib.Path(source_path)
        if not path.exists():
            content = 'file not found: ' + sub_path
        else:
            with open(source_path, 'r', encoding='utf-8') as f:
                content = f.read()

    return content

#———————————————————————————————————————— fin
