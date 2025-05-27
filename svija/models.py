
#:::::::::::::::::::::::::::::::::::::::: models.py

# model names are SINGULAR
# 252 section, permit unknown results — see link somewhere

#———————————————————————————————————————— random notes

# changing model names implies changing static/admin_extra.css

# on_delete: stackoverflow.com/questions/38388423/what-does-on-delete-do-on-django-models

#———————————————————————————————————————— imports

import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# pip install django-model-utils
from model_utils import Choices

from ckeditor.fields import RichTextField
from datetime import datetime

# for stripping chars from page › url
import re                                                                         

#———————————————————————————————————————— array: script types

script_types = (
    ('CSS',     _('css script')),
    ('head JS', _('head js script')),
    ('body JS', _('body js script')),
    ('HTML',    _('html script')),
    ('form',    _('form script')),
    )

#———————————————————————————————————————— functions to correct input

# https://stackoverflow.com/questions/36330677/django-model-set-default-charfield-in-lowercase/49181581#49181581

#   class alphaLower(models.CharField):
#       def get_prep_value(self, value):
#               return str(value).lower()

class addAiToEnd(models.CharField):
    def get_prep_value(self, value):
        if value != '':
          if value[-3:] != '.ai':                                                     
              value += '.ai'                                                            
        return value

class alphaLower(models.CharField):
    def get_prep_value(self, value):
        value = re.sub("[^A-Za-z0-9-_]","",value)
        return value.lower()

class alphaAll(models.CharField):
    def get_prep_value(self, value):
        value = re.sub("[^A-Za-z0-9-_]","",value)
        return value

class alphaStar(models.CharField):
    def get_prep_value(self, value):
        value = re.sub("[^A-Za-z0-9-_*]","",value)
        return value.lower()

class UrlField(models.CharField):                                              # deprecated, need to delete
    def get_prep_value(self, value):
        value = re.sub("[^A-Za-z0-9-_]","",value)
        return value.lower()

class slashOrHTTPS(models.CharField):         # for redirects
    def get_prep_value(self, value):
        if value[0:4] != 'http' and value[0:1] != '/':
          value = '/' + value
        return value.lower()

#———————————————————————————————————————— control · no dependencies

# _h fields are not in admin, but are updated when password is correct by cache_per_user module

class Control(models.Model): 
    limit    = models.PositiveIntegerField(default=300, verbose_name='SYNC folder MB max',)
    limit_h  = models.PositiveIntegerField(default=300, verbose_name='SYNC folder MB max',)
    used     = models.PositiveIntegerField(default=300, verbose_name='SYNC folder MB current',)
    used_h   = models.PositiveIntegerField(default=300, verbose_name='SYNC folder MB current',)
    cached   = models.BooleanField(default=False, verbose_name='cache active',)
    cached_h = models.BooleanField(default=False, verbose_name='cache active',)
    password = models.CharField(max_length=20, default='', verbose_name='password')

    def __str__(self):
        return "Site Configuration"
    class Meta:
        verbose_name = "control"
        verbose_name_plural = "Control"

#———————————————————————————————————————— redirect · no dependencies

class Redirect(models.Model): 
    enabled = models.BooleanField(default=True, verbose_name=_('redirect enabled'),)
    from_url = slashOrHTTPS(max_length=200, default='', verbose_name=_('from URL'))
#        url   = alphaLower(max_length=200, default='', verbose_name=_('address'),) 
    to_url = models.CharField(max_length=200, default='', verbose_name=_('to URL'))

    def __str__(self):
        return self.from_url
    class Meta:
        verbose_name = _("url redirect")
        verbose_name_plural = _("url redirects model list")

#———————————————————————————————————————— font · no dependencies TR

class Font(models.Model): 
    svg_ref      = models.CharField(max_length=100, default='', verbose_name=_('svg name'))
    family       = models.CharField(max_length=100, default='', verbose_name=_('font family'), blank=True)
    weight       = models.CharField(max_length=100, default='', verbose_name=_('font weight'), blank=True)
    style        = models.CharField(max_length=100, default='', verbose_name=_('font style'), blank=True)
    woff         = models.CharField(max_length=100, default='', verbose_name=_('woff name'), blank=True)

    google       = models.BooleanField(default=False, verbose_name=_('google font'),)
    enabled      = models.BooleanField(default=True, verbose_name=_('font enabled'),)
    adobe_pasted = models.CharField(max_length=300, default='', verbose_name=_('adobe link'), blank=True)
    adobe_url    = models.CharField(max_length=300, default='', verbose_name=_('adobe url'), blank=True)
    adobe_sheet  = models.TextField(max_length=99000, default='', verbose_name=_('adobe contents'), blank=True,)

    # to rename
    category = models.CharField(max_length=200, default='', verbose_name='tag', blank=True,)

    def __str__(self):
        return self.svg_ref
    class Meta:
        ordering = ['-enabled', 'category', 'family', 'style', 'svg_ref',]
        verbose_name = _("font")
        verbose_name_plural = _("font model list")

#———————————————————————————————————————— section · no dependencies

# Create or retrieve a placeholder
def get_sentinel_language():
    return Section.objects.get_or_create(name="undefined", code="na")[0]

# Create an additional method to return only the id - default expects an id and not a Model object
def get_sentinel_language_id():
    return get_sentinel_language().id

# Create or retrieve a placeholder
def get_sentinel_section():
    return Section.objects.get_or_create(name="undefined", code="na")[0]

# Create an additional method to return only the id - default expects an id and not a Model object
def get_sentinel_section_id():
    return get_sentinel_section().id


# https://stackoverflow.com/questions/73069401/how-to-get-django-admin-pulldown-list-to-just-show-the-first-order-by-item-ins
# so section pulldown will have first element selected
def get_default_section():
  return Section.objects.first()

def get_default_section_id():
  return Section.objects.first().id

class Section(models.Model):
    code     = alphaStar(max_length=20, default='', blank=False, verbose_name=_('section address'),)
    language = models.BooleanField(default=False, verbose_name=_('language code'),)
    enabled  = models.BooleanField(default=True, verbose_name=_('section enabled'),)
    name     = models.CharField(max_length=100, default='', verbose_name=_('name'),)
#   code     = models.CharField(max_length=20, default='', blank=False, verbose_name='code (visible to users)',)
    default_page = models.CharField(max_length=200, default='', verbose_name=_('default page'),blank=False,)

    order = models.PositiveSmallIntegerField(default=0, verbose_name=_('display order'),)

    title = models.CharField(max_length=100, default='', blank=True, verbose_name=_('title'),)
    touch = models.CharField(max_length=100, default='', blank=True, verbose_name=_('iphone icon'),)

    email    = models.CharField(max_length=100, default='', blank=True, verbose_name=_('destination email'),)
    bcc      = models.CharField(max_length=200, default='', verbose_name=_('bcc address'),blank=True,)
    subject  = models.CharField(max_length=200, default='', verbose_name=_('email subject'),blank=True,)

    mail_frm = models.CharField(max_length=200, default='', verbose_name=_('return address label'),blank=True,)

    # field labels
    form_name       = models.CharField(max_length=100, default='', blank=True, verbose_name=_('name label'),)
    form_business   = models.CharField(max_length=100, default='', blank=True, verbose_name=_('business label'),)
    form_email      = models.CharField(max_length=100, default='', blank=True, verbose_name=_('email label'),)
    form_message    = models.CharField(max_length=100, default='', blank=True, verbose_name=_('message label'),)
    form_send       = models.CharField(max_length=100, default='', blank=True, verbose_name=_('send label'),)

    # status messages
    form_status     = models.CharField(max_length=100, default='', blank=True, verbose_name=_('initial status'),)
    form_sending    = models.CharField(max_length=100, default='', blank=True, verbose_name=_('sending status'),)
    form_rcvd       = models.CharField(max_length=100, default='', blank=True, verbose_name=_('sent status'),)

    # alerts
    form_alert_rcvd = models.CharField(max_length=100, default='', blank=True, verbose_name=_('email sent alert'),)
    form_alert_fail = models.CharField(max_length=100, default='', blank=True, verbose_name=_('send failed alert'),)

    comment       = models.TextField(max_length=5000, default='Site built entirely in Adobe Illustrator – visit svija.com for more information!', verbose_name=_('source code message'), )

    def __str__(self):
        return self.code
    class Meta:
        ordering = ['order']
        verbose_name = _("section")
        verbose_name_plural = _("section model list")

#———————————————————————————————————————— screen · no dependencies

class Screen(models.Model):
#   code    = models.CharField(max_length=20, default='', verbose_name='artboard name',)
    code    = alphaStar(max_length=20, default='',         verbose_name=_('artboard code'),) 
    name    = models.CharField(max_length=200, default='', verbose_name=_('name'),)
    order   = models.PositiveSmallIntegerField(default=0,  verbose_name=_('display order'),)

    pixels  = models.PositiveSmallIntegerField(default=0, verbose_name=_('break point'),)
    width   = models.PositiveSmallIntegerField(default=0, verbose_name=_('artboard width'),)
    visible = models.PositiveSmallIntegerField(default=0, verbose_name=_('visible width'),)
    offsetx = models.PositiveSmallIntegerField(default=0, verbose_name=_('x offset'),)
    offsety = models.PositiveSmallIntegerField(default=0, verbose_name=_('y offset'),)

    def __str__(self):
        return self.code
    class Meta:
        ordering = ['order', 'width']
        verbose_name = _("screen size")
        verbose_name_plural = _("screen size model list")

#———————————————————————————————————————— script library · no dependencies

# to rename
class Script(models.Model):

    name         = models.CharField(max_length=200, default='', verbose_name=_('script library name'),)
    enabled      = models.BooleanField(default=True, verbose_name=_('enabled'),)
    always       = models.BooleanField(default=False, verbose_name=_('always include'),)
    # to rename
    category     = models.CharField(max_length=100, default='', verbose_name='tag', blank=True,)
    url          = models.CharField(max_length=120, default='',blank=True,  verbose_name=_('instructions link'),)
#   instructions = models.TextField(max_length=2000, default='', blank=True, verbose_name=_('instructions notes'),)
    instructions = RichTextField(default='', blank=True, verbose_name=_('instructions notes'),)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-enabled', 'category', 'name', ]
        verbose_name = _("script library")
        verbose_name_plural = _("script library model list")

#———————————————————————————————————————— script library scripts · script

class ScriptScripts(models.Model):
    script  = models.ForeignKey(Script, on_delete=models.CASCADE)
    type    = models.CharField(max_length=255, default='', choices=Choices(*script_types), verbose_name=_('script type'),)
    name    = models.CharField(max_length=200, default='', verbose_name=_('script name'),)
    content = models.TextField(max_length=200000, default='', verbose_name=_('script content'),)
    order   = models.IntegerField(default=0, verbose_name=_('load order'),)
    enabled = models.BooleanField(default=True, verbose_name=_('enabled'),)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ["order"]
        # only seen when deleting a script library, as a dependency
        verbose_name = _("included script")
        verbose_name_plural = _("included script")

#———————————————————————————————————————— module· no dependencies

positions = (
    ('attached', _("position attached")),
    ('floating', _("position floating")),
    ('none', _("position none")),
    )

corners = (
    ('top left', _("top left")),
    ('top right', _("top right")),
    ('bottom left', _("bottom left")),
    ('bottom right', _("bottom right")),
    )

class Module(models.Model):

    name      = models.CharField(max_length=200, default='', verbose_name=_('name'),)
    enabled = models.BooleanField(default=True, verbose_name=_('enabled'),)

    always    = models.BooleanField(default=False, verbose_name=_('always include'),)
    screen    = models.ForeignKey(Screen, default=1, on_delete=models.PROTECT, verbose_name=_('screen size'),)
    section   = models.ForeignKey(Section, default=get_default_section, on_delete=models.PROTECT, verbose_name=_('section'))
    # to rename
    tag       = models.CharField(max_length=100, default='', verbose_name='tag', blank=True,)
    zindex    = models.SmallIntegerField(default=0, verbose_name=_('z index'),)

    css_id = models.CharField(max_length=200, default='', verbose_name=_('css id'), blank=True,)
    filename = models.CharField(max_length=200, default='', blank=True, verbose_name=_('illustrator file'),)
#   filename = addAiToEnd(max_length=200, default='', blank=True, verbose_name='Illustrator file',)

#lass addAiToEnd(models.CharField):

    url          = models.CharField(max_length=120, default='',blank=True,  verbose_name=_('instructions link'),)
    #nstructions = models.TextField(max_length=2000, default='', blank=True, verbose_name=_('instructions notes'),)
    instructions = RichTextField(default='', blank=True, verbose_name=_('instructions notes'),)

    position = models.CharField(max_length=255, default='attached', choices=Choices(*positions), verbose_name=_('floating attached'),)
    corner   = models.CharField(max_length=255, default='top left', choices=Choices(*corners), verbose_name=_('corner position'),)
    offsetx  = models.FloatField(default=0, verbose_name=_('x offset'),)
    offsety  = models.FloatField(default=0, verbose_name=_('y offset'),)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-enabled', 'name', 'section', 'screen', ]
        verbose_name = "module"
        verbose_name_plural = _("module model list")

#———————————————————————————————————————— module scripts · no dependencies

class ModuleScript(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, default='', choices=Choices(*script_types), verbose_name=_('script type'),)
    name = models.CharField(max_length=200, default='', verbose_name=_('script name'),)
    content = models.TextField(max_length=50000, default='', verbose_name=_('script content'),)
    order = models.IntegerField(default=0, verbose_name=_('load order'),)
    enabled = models.BooleanField(default=True, verbose_name=_('enabled'),)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ["order"]
        verbose_name = _("included script")
        verbose_name_plural = _("included scripts")

#———————————————————————————————————————— robots · no dependencies

class Robots(models.Model):
    name = models.CharField(max_length=200, default='', verbose_name=_('name'), )
    contents = models.TextField(max_length=5000, default='', verbose_name=_('contents'),blank=True,)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']
        verbose_name = _("robots.txt file")
        verbose_name_plural = _("robots model list")

#———————————————————————————————————————— settings · section & robots

def get_sentinel_robots():                                                        # deprecated, need to delete
    return Robots.objects.get_or_create(name="undefined",contents="n/a")[0]

def get_sentinel_robots_id():                                                     # deprecated, need to delete
    return get_sentinel_robots().id

def get_default_robots():
  return Robots.objects.first()

def get_default_robots_id():               # this is the problem
  return Robots.objects.first().id

class Settings(models.Model):

    # https://stackoverflow.com/a/67298691/72958 & see section model for other necessary parts
    robots        = models.ForeignKey(Robots,  default=get_default_robots_id,  blank=True, on_delete=models.SET(get_default_robots),  verbose_name='robots.txt')
    #ection       = models.ForeignKey(Section, default=get_default_section, on_delete=get_default_section, verbose_name='default section')
    section       = models.ForeignKey(Section, default=get_sentinel_section_id, on_delete=models.SET(get_sentinel_section), verbose_name=_('default section'))

    enabled       = models.BooleanField(default=True, verbose_name=_('on line'),)
    url           = models.CharField(max_length=200, default='', verbose_name=_('site url'),)
    p3_color      = models.BooleanField(default=True, verbose_name=_('display p3'),)

    analytics_id  = models.CharField(max_length=200, default='', verbose_name=_('analytics id'),blank=True,)
    tracking_on   = models.BooleanField(default=False, verbose_name=_('cookies allowed'),)
    maps_api_key  = models.CharField(max_length=200, default='', verbose_name=_('maps api key'),blank=True,)

    # color settings
    color_main     = models.CharField(max_length=80, default='rgb(70%, 100%, 0%)', verbose_name=_('main color'),blank=True,)
    color_accent   = models.CharField(max_length=80, default='rgb(87%, 100%, 60% )', verbose_name=_('accent color'),blank=True,)
    color_dark     = models.CharField(max_length=80, default='rgb(15%, 15%, 15% )', verbose_name=_('dark color'),blank=True,)

    # email settings
    mail_id       = models.CharField(max_length=200, default='', verbose_name=_('email username'),    blank=True,)
    mail_pass     = models.CharField(max_length=200, default='', verbose_name=_('email password'),    blank=True,)
    mail_srv      = models.CharField(max_length=200, default='', verbose_name=_('email server'),      blank=True,)
    mail_port     = models.IntegerField(             default=0,  verbose_name=_('email server port'), blank=True, null=True,)
    mail_tls      = models.BooleanField(default=True, verbose_name=_('use tls'),)
    notes         = models.TextField(max_length=2000, default='', blank=True, verbose_name=_('notes'),)

   # @admin.display(description=_('Is it a mouse?'))
    def __str__(self):
        return self.url
    class Meta:
        verbose_name = _("website")
        verbose_name_plural = _("website settings model list")

#———————————————————————————————————————— Page · uses template & prefix

class Page(models.Model): 

    published = models.BooleanField(default=True, verbose_name=_('enabled'),)
    screen    = models.ForeignKey(Screen, default=1, on_delete=models.PROTECT, verbose_name=_('screen size'),)
    section   = models.ForeignKey(Section, default=get_default_section, on_delete=models.PROTECT, verbose_name=_('section'),)
#   url       = models.CharField(max_length=200, default='', verbose_name='address')
    url       = alphaLower(max_length=200, default='', verbose_name=_('address'),) 

    # to rename
    category  = models.CharField(max_length=200, default='', verbose_name='tag', blank=True,)

    # meta
    notes     = models.TextField(max_length=2000, default='', blank=True, verbose_name=('notes'),)
    pub_date  = models.DateTimeField(default=datetime.now, blank=True, verbose_name=_('publication date'),)

    # used in page construction
    title  = models.CharField(max_length=200, default='', blank=True, verbose_name=_('title'),)

    # accessibility
    accessibility_name = models.CharField(max_length=200, default='', blank=True, verbose_name=_('link name'),)
    accessibility_text = RichTextField(verbose_name=_('accessibility content'), blank=True)

    incl_modules = models.BooleanField(default=True, verbose_name=_('default modules'),)
    incl_scripts = models.BooleanField(default=True, verbose_name=_('default scripts'),)

    module = models.ManyToManyField(Module, through='PageModule')
    script = models.ManyToManyField(Script, through='PageScript')

    default_dims = models.BooleanField(default=True, verbose_name=_('default dimensions'),)
    width    = models.PositiveSmallIntegerField(default=0, verbose_name=_('artboard width'),)
    visible  = models.PositiveSmallIntegerField(default=0, verbose_name=_('visible width'),)
    offsetx  = models.PositiveSmallIntegerField(default=0, verbose_name=_('x offset'),)
    offsety  = models.PositiveSmallIntegerField(default=0, verbose_name=_('y offset'),)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.url
    class Meta:
        ordering = ['-published', 'url', 'section', 'screen', '-pub_date', ]
        verbose_name_plural = _("page")
        verbose_name_plural = _("page model list")
    eache_reset   = models.BooleanField(default=False, verbose_name='delete cache (or visit example.com/c)',)

#———————————————————————————————————————— Page models

# foreignkey, available sitewide
class PageModule(models.Model):
    page   = models.ForeignKey(Page,   on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    zindex = models.SmallIntegerField(default=0, verbose_name=_('z index'),)
    enabled = models.BooleanField(default=True, verbose_name=_('enabled'),)
    def __str__(self):
        return self.module.name
    class Meta:
        verbose_name = _("link to module")
        verbose_name_plural = _("links to modules")
        ordering = ["zindex"]

# foreignkey, available sitewide
class PageScript(models.Model):
    page   = models.ForeignKey(Page,   on_delete=models.CASCADE)
    script = models.ForeignKey(Script, on_delete=models.CASCADE, verbose_name=_('script library'),)
    enabled = models.BooleanField(default=True, verbose_name=_('enabled'),)
    def __str__(self):
        return self.script.name
    class Meta:
        verbose_name = _("link to script")
        verbose_name_plural = _("links to script")
        ordering = ["script"]

class Illustrator(models.Model):
#   page = models.ForeignKey(Page, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name = 'illustrator_fk')
    filename = models.CharField(max_length=200, default='', verbose_name=_('file name'),)
#   filename = addAiToEnd(max_length=200, default='')
    zindex = models.SmallIntegerField(default=0, verbose_name=_('z index'),)
    enabled = models.BooleanField(default=True, verbose_name=_('enabled'),)
    def __str__(self):
        return self.filename
    class Meta:
        verbose_name = _("illustrator file")
        verbose_name_plural = _("illustrator files")
        ordering = ["zindex"]

class AdditionalScript(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, default='', choices=Choices(*script_types), verbose_name=_('script type'),)
    name = models.CharField(max_length=200, default='', verbose_name=_('name'),)
    content = models.TextField(max_length=50000, default='', verbose_name=_('contents'),)
    order = models.IntegerField(default=0, verbose_name=_('load order'),)
    enabled = models.BooleanField(default=True, verbose_name=_('enabled'),)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ["order"]
        verbose_name = _("script")
        verbose_name_plural = _("scripts")


#:::::::::::::::::::::::::::::::::::::::: fin

