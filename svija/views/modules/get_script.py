
#———————————————————————————————————————— add a script, returns string
# add a script (supplied or from file)
# with comment including it's name
# used in sort_modules

import os
import pathlib
import re

def get_script(kind, name, content):

    # https://regex101.com
    # matches a-z   0-9   \s   .   _   +   -   &  .ext (2 or 3 letters)
    filename = re.compile("^[a-z,0-9,\s,\.,_,+,\-,&]+\.[a-z]{2,3}$", re.I) 

    if filename.match(content):
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

#———————————————————————————————————————— validate email / telephone

#   whitelisttel  = re.compile("^\+?[0-9,\-,\.,' ',\(,\)]+$") # https://regex101.com
#   whitelistmail = re.compile("[a-z,0-9,\.,_,-]+\@[a-z,0-9,\.,-]+\.[a-z]+")

#   blacklist = ".*[\\|\^|\$|\||\*|\+|\[|\{|<|>]+.*"

#   if not whitelisttel.match(addr) and not whitelistmail.match(addr):
#       fail += ' E1'; body = 'ADDRESS FAILED WHITELIST. ' + body

#   if re.match(blacklist, naim):
#       fail += ' E2'; body = 'NAME FAILED BLACKLIST. ' + body

#   if re.match(blacklist, body):
#       fail += ' E3'; body = 'MESSAGE FAILED BLACKLIST. ' + body

#   #———————————————————————————————————————— if fail get out
