#:::::::::::::::::::::::::::::::::::::::: models.py

# model names are SINGULAR
# 252 section, permit unknown results — see link somewhere

#———————————————————————————————————————— random notes

# changing model names implies changing static/admin_extra.css

# on_delete: stackoverflow.com/questions/38388423/what-does-on-delete-do-on-django-models

#———————————————————————————————————————— imports

from django.db import models
import datetime
from django.utils import timezone

# pip install django-model-utils
from model_utils import Choices

from ckeditor.fields import RichTextField
from datetime import datetime

# for stripping chars from page › url
import re                                                                         

#———————————————————————————————————————— array: types of scripts

script_types = ('CSS', 'head JS', 'body JS', 'HTML', 'form',)

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

class UrlField(models.CharField):                                              # deprecated, need to delete
    def get_prep_value(self, value):
        value = re.sub("[^A-Za-z0-9-_]","",value)
        return value.lower()

#———————————————————————————————————————— Control · no dependencies

# _h fields are not in admin, but are updated when password is correct by cache_per_user module

class Control(models.Model): 
    limit    = models.PositiveIntegerField(default=300, verbose_name='sync folder MB max',)
    limit_h  = models.PositiveIntegerField(default=300, verbose_name='sync folder MB max',)
    used     = models.PositiveIntegerField(default=300, verbose_name='sync folder MB current',)
    used_h   = models.PositiveIntegerField(default=300, verbose_name='sync folder MB current',)
    cached   = models.BooleanField(default=False, verbose_name='cache active',)
    cached_h = models.BooleanField(default=False, verbose_name='cache active',)
    password = models.CharField(max_length=20, default='', verbose_name='password')

    def __str__(self):
        return "Site Configuration"
    class Meta:
        verbose_name = "control"
        verbose_name_plural = "Control"

#———————————————————————————————————————— Redirect · no dependencies

class Redirect(models.Model): 
    enabled = models.BooleanField(default=True, verbose_name='enabled',)
    from_url = models.CharField(max_length=200, default='', verbose_name='old URL')
    to_url = models.CharField(max_length=200, default='', verbose_name='new URL')

    def __str__(self):
        return self.from_url
    class Meta:
        verbose_name = "redirect"
        verbose_name_plural = "3.2 · Redirects"

#———————————————————————————————————————— Font · no dependencies

class Font(models.Model): 
    svg_ref      = models.CharField(max_length=100, default='', verbose_name='SVG name')
    family       = models.CharField(max_length=100, default='', verbose_name='family', blank=True)
    weight       = models.CharField(max_length=100, default='', verbose_name='weight', blank=True)
    style        = models.CharField(max_length=100, default='', verbose_name='style', blank=True)
    woff         = models.CharField(max_length=100, default='', verbose_name='WOFF filename', blank=True)

    google       = models.BooleanField(default=False, verbose_name='Google font',)
    enabled      = models.BooleanField(default=True, verbose_name='enabled',)
    adobe_pasted = models.CharField(max_length=300, default='', verbose_name='pasted Adobe link', blank=True)
    adobe_url    = models.CharField(max_length=300, default='', verbose_name='font file URL', blank=True)
    adobe_sheet  = models.TextField(max_length=99000, default='', verbose_name='link contents', blank=True,)

		# to rename
    category = models.CharField(max_length=200, default='', verbose_name='tag (optional)', blank=True,)

    def __str__(self):
        return self.svg_ref
    class Meta:
        verbose_name = "font"
        verbose_name_plural = "2.3 · Fonts"
        ordering = ['-enabled', 'category', 'family', 'style', 'svg_ref',]

#———————————————————————————————————————— Section · no dependencies

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
    code = alphaLower(max_length=20, default='', blank=False, verbose_name='address',)
    name = models.CharField(max_length=100, default='', verbose_name='description',)
#   code = models.CharField(max_length=20, default='', blank=False, verbose_name='code (visible to users)',)
    default_page = models.CharField(max_length=200, default='', verbose_name='default page',blank=False,)

    order = models.PositiveSmallIntegerField(default=0, verbose_name='display order')

    title = models.CharField(max_length=100, default='', blank=True, verbose_name='section title',)
    touch = models.CharField(max_length=100, default='', blank=True, verbose_name='iPhone icon name',)

    email    = models.CharField(max_length=100, default='', blank=True, verbose_name='destination email',)
    bcc      = models.CharField(max_length=200, default='', verbose_name='bcc address',blank=True,)
    subject  = models.CharField(max_length=200, default='', verbose_name='email subject',blank=True,)

    mail_frm = models.CharField(max_length=200, default='', verbose_name='return address label',blank=True,)

    # field labels
    form_name       = models.CharField(max_length=100, default='', blank=True, verbose_name='name',)
    form_business   = models.CharField(max_length=100, default='', blank=True, verbose_name='business',)
    form_email      = models.CharField(max_length=100, default='', blank=True, verbose_name='email',)
    form_message    = models.CharField(max_length=100, default='', blank=True, verbose_name='message',)
    form_send       = models.CharField(max_length=100, default='', blank=True, verbose_name='send button',)

    # status messages
    form_status     = models.CharField(max_length=100, default='', blank=True, verbose_name='initial status',)
    form_sending    = models.CharField(max_length=100, default='', blank=True, verbose_name='while sending',)
    form_rcvd       = models.CharField(max_length=100, default='', blank=True, verbose_name='email sent',)

    # alerts
    form_alert_rcvd = models.CharField(max_length=100, default='', blank=True, verbose_name='email sent (alert)',)
    form_alert_fail = models.CharField(max_length=100, default='', blank=True, verbose_name='send failed (alert)',)

    comment       = models.TextField(max_length=5000, default='Site built entirely in SVG with Svija – visit svija.love for more information!', verbose_name='source code message', )

    def __str__(self):
        return self.code
    class Meta:
        ordering = ['order']
        verbose_name_plural = "1.2 · Sections"

#———————————————————————————————————————— Screen · no dependencies

class Screen(models.Model):
#   code    = models.CharField(max_length=20, default='', verbose_name='artboard name',)
    code     = alphaLower(max_length=20, default='', verbose_name='artboard name') 
    name    = models.CharField(max_length=200, default='', verbose_name='description')
    order   = models.PositiveSmallIntegerField(default=0, verbose_name='display order')

    pixels  = models.PositiveSmallIntegerField(default=0, verbose_name='break point',)
    width   = models.PositiveSmallIntegerField(default=0, verbose_name='artboard width',)
    visible = models.PositiveSmallIntegerField(default=0, verbose_name='visible width')
    offsetx = models.PositiveSmallIntegerField(default=0, verbose_name='offset x')
    offsety = models.PositiveSmallIntegerField(default=0, verbose_name='offset y')

    def __str__(self):
        return self.code
    class Meta:
        ordering = ['order', 'width']
        verbose_name = "screen size"
        verbose_name_plural = "1.3 · Screen Sizes"

#———————————————————————————————————————— Script Set · no dependencies

# to rename
class Script(models.Model):

    name         = models.CharField(max_length=200, default='')
    enabled      = models.BooleanField(default=True, verbose_name='enabled',)
    always       = models.BooleanField(default=False, verbose_name='always include',)
		# to rename
    category     = models.CharField(max_length=100, default='', verbose_name='tag (optional)', blank=True,)
    url          = models.CharField(max_length=120, default='',blank=True,  verbose_name='link',)
    instructions = models.TextField(max_length=2000, default='', blank=True, verbose_name='notes',)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-enabled', 'category', 'name', ]
        verbose_name_plural = "3.1 · Script Sets"

#———————————————————————————————————————— Script Set Scripts · script

class ScriptScripts(models.Model):
    script  = models.ForeignKey(Script, on_delete=models.CASCADE)
    type    = models.CharField(max_length=255, default='', choices=Choices(*script_types), verbose_name='type')
    name    = models.CharField(max_length=200, default='')
    content = models.TextField(max_length=200000, default='', verbose_name='content',)
    order   = models.IntegerField(default=0, verbose_name='load order')
    enabled = models.BooleanField(default=True, verbose_name='enabled',)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "included script"
        verbose_name_plural = "included scripts"
        ordering = ["order"]

#———————————————————————————————————————— Module · no dependencies

positions = ('attached', 'floating', 'none',)
corners = ('top left', 'top right', 'bottom left', 'bottom right',)

class Module(models.Model):

    name      = models.CharField(max_length=200, default='')
    enabled = models.BooleanField(default=True, verbose_name='enabled',)

    always    = models.BooleanField(default=False, verbose_name='always include',)
    screen    = models.ForeignKey(Screen, default=1, on_delete=models.PROTECT, verbose_name='screen size',)
    section   = models.ForeignKey(Section, default=get_default_section, on_delete=models.PROTECT, verbose_name='section')
		# to rename
    category = models.CharField(max_length=100, default='', verbose_name='tag (optional)', blank=True,)
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Z-index')

    css_id = models.CharField(max_length=200, default='', verbose_name='object ID (optional)', blank=True,)
#   filename = models.CharField(max_length=200, default='', blank=True, verbose_name='Illustrator file',)
    filename = addAiToEnd(max_length=200, default='', blank=True, verbose_name='Illustrator file',)

#lass addAiToEnd(models.CharField):

    url          = models.CharField(max_length=120, default='',blank=True,  verbose_name='link',)
    instructions = models.TextField(max_length=2000, default='', blank=True, verbose_name='notes',)

    position = models.CharField(max_length=255, default='attached', choices=Choices(*positions), verbose_name='position')
    corner   = models.CharField(max_length=255, default='top left', choices=Choices(*corners), verbose_name='relative to')
    offsetx  = models.FloatField(default=0, verbose_name='horizontal offset (px)',)
    offsety  = models.FloatField(default=0, verbose_name='vertical offset (px)',)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-enabled', 'name', 'section', 'screen', ]
        verbose_name_plural = "2.1 · Modules"

#———————————————————————————————————————— module scripts · no dependencies

class ModuleScript(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, default='', choices=Choices(*script_types), verbose_name='type')
    name = models.CharField(max_length=200, default='')
    content = models.TextField(max_length=50000, default='', verbose_name='content',)
    order = models.IntegerField(default=0, verbose_name='load order')
    enabled = models.BooleanField(default=True, verbose_name='enabled',)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "included script"
        verbose_name_plural = "included scripts"
        ordering = ["order"]

#———————————————————————————————————————— Robots · no dependencies

class Robots(models.Model):
    name = models.CharField(max_length=200, default='')
    contents = models.TextField(max_length=5000, default='', verbose_name='file contents',blank=True,)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']
        verbose_name = "robots.txt"
        verbose_name_plural = "3.3 · Robots.txt"

#———————————————————————————————————————— Settings · Section & Robots

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
    section       = models.ForeignKey(Section, default=get_sentinel_section_id, on_delete=models.SET(get_sentinel_section), verbose_name='default section')

    enabled       = models.BooleanField(default=True, verbose_name='online',)
    url           = models.CharField(max_length=200, default='', verbose_name='site address',)
    p3_color      = models.BooleanField(default=True, verbose_name='use "Display P3" color space where possible',)

    analytics_id  = models.CharField(max_length=200, default='', verbose_name='analytics ID',blank=True,)
    tracking_on   = models.BooleanField(default=False, verbose_name='cookies allowed by default',)
    maps_api_key  = models.CharField(max_length=200, default='', verbose_name='Google Maps API key',blank=True,)

    # email settings
    mail_id       = models.CharField(max_length=200, default='', verbose_name='username for sending email',blank=True,)
    mail_pass     = models.CharField(max_length=200, default='', verbose_name='password for sending email',blank=True,)
    mail_srv      = models.CharField(max_length=200, default='', verbose_name='server for sending email',blank=True,)
    mail_port     = models.IntegerField(default=0, verbose_name='email server port', null=True, blank=True,)
    mail_tls      = models.BooleanField(default=True, verbose_name='use TLS',)

    def __str__(self):
        return self.url
    class Meta:
        verbose_name = "website"
        verbose_name_plural = "1.1 · URL & Settings"

#———————————————————————————————————————— Page · uses template & prefix

class Page(models.Model): 

    published = models.BooleanField(default=True, verbose_name='published',)
    screen    = models.ForeignKey(Screen, default=1, on_delete=models.PROTECT, verbose_name='screen size',)
    section   = models.ForeignKey(Section, default=get_default_section, on_delete=models.PROTECT, verbose_name='section',)
#   url       = models.CharField(max_length=200, default='', verbose_name='address')
    url       = alphaLower(max_length=200, default='', verbose_name='address') 

		# to rename
    category  = models.CharField(max_length=200, default='', verbose_name='tag (optional)', blank=True,)

    # meta
    notes     = models.TextField(max_length=2000, default='', blank=True)
    pub_date  = models.DateTimeField(default=datetime.now, blank=True, verbose_name='publication date',)

    # used in page construction
    title  = models.CharField(max_length=200, default='', blank=True)

    # accessibility
    accessibility_name = models.CharField(max_length=200, default='', blank=True, verbose_name='link name')
    accessibility_text = RichTextField(verbose_name='accessibility content', blank=True)

    incl_modules = models.BooleanField(default=True, verbose_name='default modules',)
    incl_scripts = models.BooleanField(default=True, verbose_name='default scripts',)

    module = models.ManyToManyField(Module, through='PageModule')
    script = models.ManyToManyField(Script, through='PageScript')

    default_dims = models.BooleanField(default=True, verbose_name='default dimensions',)
    width    = models.PositiveSmallIntegerField(default=0, verbose_name='artboard width')
    visible  = models.PositiveSmallIntegerField(default=0, verbose_name='visible width')
    offsetx  = models.PositiveSmallIntegerField(default=0, verbose_name='offset x')
    offsety  = models.PositiveSmallIntegerField(default=0, verbose_name='offset y')

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.url
    class Meta:
        ordering = ['-published', 'url', 'section', 'screen', '-pub_date', ]
        verbose_name_plural = "2.2 · Pages"
    eache_reset   = models.BooleanField(default=False, verbose_name='delete cache (or visit example.com/c)',)

#———————————————————————————————————————— Page models

# foreignkey, available sitewide
class PageModule(models.Model):
    page   = models.ForeignKey(Page,   on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    zindex = models.IntegerField(default=0, verbose_name='z index')
    enabled = models.BooleanField(default=True, verbose_name='enabled',)
    def __str__(self):
        return self.module.name
    class Meta:
        verbose_name = "link to module"
        verbose_name_plural = "links to modules"
        ordering = ["zindex"]

# foreignkey, available sitewide
class PageScript(models.Model):
    page   = models.ForeignKey(Page,   on_delete=models.CASCADE)
    script = models.ForeignKey(Script, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True, verbose_name='enabled',)
    def __str__(self):
        return self.script.name
    class Meta:
        verbose_name = "link to script"
        verbose_name_plural = "links to script"
        ordering = ["script"]

class Illustrator(models.Model):
#   page = models.ForeignKey(Page, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name = 'illustrator_fk')
#   filename = models.CharField(max_length=200, default='')
    filename = addAiToEnd(max_length=200, default='')
    zindex = models.IntegerField(default=0, verbose_name='z index')
    enabled = models.BooleanField(default=True, verbose_name='enabled',)
    def __str__(self):
        return self.filename
    class Meta:
        verbose_name = "Illustrator file"
        verbose_name_plural = "Illustrator files"
        ordering = ["zindex"]

class AdditionalScript(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, default='', choices=Choices(*script_types), verbose_name='type')
    name = models.CharField(max_length=200, default='')
    content = models.TextField(max_length=50000, default='', verbose_name='content',)
    order = models.IntegerField(default=0, verbose_name='load order')
    enabled = models.BooleanField(default=True, verbose_name='enabled',)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "additional script"
        verbose_name_plural = "additional scripts"
        ordering = ["order"]


#:::::::::::::::::::::::::::::::::::::::: fin
