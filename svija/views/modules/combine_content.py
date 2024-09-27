#———————————————————————————————————————— views/modules/combine_content.py

# accepts a list of content blocks that each contain 6 elements

def combine_content(blocks):

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

    return { 'head_js':head_js, 'css':css, 'body':body, }

#———————————————————————————————————————— fin
