#———————————————————————————————————————— PageObject.py

#———————————————————————————————————————— notes
#
#
#———————————————————————————————————————— class page_obj():
# must be here because this file has to come first in __init__.py
# and it needs access to page_obj

class page_obj():

  def __init__(self, head_js, css, body_js, svgs, html, form):
    self.head_js  = head_js
    self.css      = css
    self.body_js  = body_js
    self.svgs     = svgs
    self.html     = html
    self.form     = form

  def __getitem__(cls, x):
    return getattr(cls, x)


#———————————————————————————————————————— fin
