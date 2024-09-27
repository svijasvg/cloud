#———————————————————————————————————————— views/modules/combine_content.py

#   accepts a list of content blocks that each contain 6 elements

#   returns 3-element dict: head_js, css, body

def combine_content(blocks, prefix):

    head_js = css = body = ''

    for i in blocks:
        head_js   += i['head_js']
        css       += i['css']
        body      += i['svgs']
        body      += i['html']
        body      += i['form']

#———————————————————————————————————————— javascript is included just after content

    for i in blocks:
        if i['body_js'] != '':
            body += '<script>' + i['body_js'] + '</script>'

    return { prefix+'_head_js':head_js, prefix+'_css':css, prefix+'_body':body, }

#———————————————————————————————————————— fin
