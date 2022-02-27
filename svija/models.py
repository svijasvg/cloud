#———————————————————————————————————————— models.py

# model names are SINGULAR

#———————————————————————————————————————— notes about this document

# CHANGING MODEL NAMES IMPLIES CHANGING STATIC/ADMIN_EXTRA.CSS

# on_delete
#https://stackoverflow.com/questions/38388423/what-does-on-delete-do-on-django-models

#———————————————————————————————————————— imports

from django.db import models
import datetime
from django.utils import timezone

# pip install django-model-utils
from model_utils import Choices

#———————————————————————————————————————— array: types of scripts

script_types = ('CSS', 'head JS', 'body JS', 'HTML', 'form',)

#———————————————————————————————————————— Redirect · no dependencies

class Redirect(models.Model): 
    active = models.BooleanField(default=True, verbose_name='active',)
    from_url = models.CharField(max_length=200, default='', verbose_name='old URL')

    # renma to_url
    to_page = models.CharField(max_length=200, default='', verbose_name='new URL')

    def __str__(self):
        return self.from_url
    class Meta:
        verbose_name = "redirect"
        verbose_name_plural = "3.2 · Redirects"

#———————————————————————————————————————— Font · no dependencies

class Font(models.Model): 
    css    = models.CharField(max_length=100, default='', verbose_name='SVG name')
    family = models.CharField(max_length=100, default='', verbose_name='family', blank=True)
    style  = models.CharField(max_length=100, default='', verbose_name='weightStyle', blank=True)
    source = models.CharField(max_length=100, default='—', verbose_name='WOFF filename', blank=True)
    google = models.BooleanField(default=True, verbose_name='Google font',)
    active = models.BooleanField(default=True, verbose_name='active',)
    category    = models.CharField(max_length=200, default='Main', verbose_name='category', blank=True,)

    def __str__(self):
        return self.css
    class Meta:
        verbose_name = "font"
        verbose_name_plural = "2.3 · Fonts"
        ordering = ['-active', 'category', 'family', 'style']

#———————————————————————————————————————— Language · no dependencies

class Language(models.Model):
    name = models.CharField(max_length=100, default='')
    code = models.CharField(max_length=20, default='', blank=True, verbose_name='code (visible to users)',)

    #efault = models.CharField(max_length=20, default='', verbose_name='default page')
    default  = models.CharField(max_length=200, default='', verbose_name='default page',blank=True,)
    display_order = models.PositiveSmallIntegerField(default=0, verbose_name='display order')

    title = models.CharField(max_length=100, default='', verbose_name='second part of page title',)
    touch = models.CharField(max_length=100, default='', blank=True, verbose_name='iPhone icon name',)

    email    = models.CharField(max_length=100, default='', blank=True, verbose_name='destination address',)
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

    comment       = models.TextField(max_length=5000, default='Site built entirely in SVG with Svija – visit svija.com for more information!', verbose_name='source code message', )

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['display_order']
        verbose_name_plural = "1.2 · Languages"

#———————————————————————————————————————— Screen · no dependencies

class Screen(models.Model):
    name = models.CharField(max_length=200, default='')
    code = models.CharField(max_length=2, default='', blank=True, verbose_name='two-letter code',)
    limit = models.PositiveSmallIntegerField(default=0, verbose_name='maximum pixel width',blank=True,)


    display_order = models.PositiveSmallIntegerField(default=0, verbose_name='display order')

    width   = models.PositiveSmallIntegerField(default=0, verbose_name='Illustrator pixel width',blank=True,)
    visible = models.PositiveSmallIntegerField(default=0, verbose_name='visible width in pixels')
    offsetx = models.PositiveSmallIntegerField(default=0, verbose_name='offset x in pixels')
    offsety = models.PositiveSmallIntegerField(default=0, verbose_name='offset y in pixels')

    # not currently implemented, so hidden
    img_multiply = models.DecimalField(default=2.4, max_digits=2, decimal_places=1, verbose_name='resolution multiple')
    img_quality  = models.PositiveSmallIntegerField(default=0, verbose_name='JPG quality (0-100)')

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['display_order']
        verbose_name = "screen size"
        verbose_name_plural = "1.3 · Screen Sizes"

#———————————————————————————————————————— Robots · no dependencies

class Robots(models.Model):
    name = models.CharField(max_length=200, default='')
    contents = models.TextField(max_length=5000, default='', verbose_name='file contents',blank=True,)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "robots.txt"
        verbose_name_plural = "3.3 · Robots.txt"

#———————————————————————————————————————— Script · no dependencies

class Script(models.Model):

    name = models.CharField(max_length=200, default='')
    active = models.BooleanField(default=True, verbose_name='active',)
    sort = models.CharField(max_length=100, default='', verbose_name='sort label (optional)', blank=True,)

    url = models.CharField(max_length=60, default='',blank=True,  verbose_name='link',)
    instructions = models.TextField(max_length=2000, default='', blank=True, verbose_name='notes',)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-active', 'sort', 'name', ]
        verbose_name_plural = "3.1 · Scripts"

#———————————————————————————————————————— script scripts · script

class ScriptScripts(models.Model):
    script = models.ForeignKey(Script, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, default='', choices=Choices(*script_types), verbose_name='type')
    name = models.CharField(max_length=200, default='')
    content = models.TextField(max_length=50000, default='', verbose_name='content',)
    order = models.IntegerField(default=0, verbose_name='load order')
    active = models.BooleanField(default=True, verbose_name='active',)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "included script"
        verbose_name_plural = "included scripts"
        ordering = ["order"]

#———————————————————————————————————————— Module · no dependencies

positions = ('absolute', 'floating', 'none',)
corners = ('top left', 'top right', 'bottom left', 'bottom right',)

class Module(models.Model):

    name = models.CharField(max_length=200, default='')
    published = models.BooleanField(default=True, verbose_name='published',)
    optional = models.BooleanField(default=False, verbose_name='always include',)
    screen = models.ForeignKey(Screen, default=1, on_delete=models.PROTECT, verbose_name='screen size',)
    language = models.ForeignKey(Language, default=3, on_delete=models.PROTECT, verbose_name='language')
    sort1 = models.CharField(max_length=100, default='Main', verbose_name='category', blank=True,)
    display_order = models.PositiveSmallIntegerField(default=0, verbose_name='Z-index')
    css_id = models.CharField(max_length=200, default='', verbose_name='object ID (optional)', blank=True,)
    filename = models.CharField(max_length=200, default='', blank=True, verbose_name='Illustrator file (optional)',)
    url = models.CharField(max_length=60, default='',blank=True,  verbose_name='link',)
    instructions = models.TextField(max_length=2000, default='', blank=True, verbose_name='notes',)

    position = models.CharField(max_length=255, default='absolute', choices=Choices(*positions), verbose_name='placement')
    corner = models.CharField(max_length=255, default='top left', choices=Choices(*corners), verbose_name='relative to')
    horz_offset = models.FloatField(default=0, verbose_name='horizontal offset (px)',)
    vert_offset = models.FloatField(default=0, verbose_name='vertical offset (px)',)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-published', 'sort1', 'name', 'screen',]
        verbose_name_plural = "2.1 · Modules"

#———————————————————————————————————————— module scripts · no dependencies

class ModuleScript(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, default='', choices=Choices(*script_types), verbose_name='type')
    name = models.CharField(max_length=200, default='')
    content = models.TextField(max_length=50000, default='', verbose_name='content',)
    order = models.IntegerField(default=0, verbose_name='load order')
    active = models.BooleanField(default=True, verbose_name='active',)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "included script"
        verbose_name_plural = "included scripts"
        ordering = ["order"]

#———————————————————————————————————————— settings · combination code & robots

class Settings(models.Model):

    active        = models.BooleanField(default=False, verbose_name='online',)
    robots        = models.ForeignKey(Robots, default=0, on_delete=models.PROTECT, verbose_name='robots.txt')
    url           = models.CharField(max_length=200, default='', verbose_name='site address',)
    p3_color      = models.BooleanField(default=True, verbose_name='use "Display P3" color space where possible',)
    language      = models.ForeignKey(Language, default=3, on_delete=models.PROTECT, verbose_name='default language')

    analytics_id  = models.CharField(max_length=200, default='', verbose_name='analytics ID',blank=True,)
    tracking_on   = models.BooleanField(default=False, verbose_name='cookies allowed by default',)
    maps_api_key  = models.CharField(max_length=200, default='', verbose_name='Google Maps API key',blank=True,)

    # email settings
    mail_id       = models.CharField(max_length=200, default='', verbose_name='username for sending email',blank=True,)
    mail_pass     = models.CharField(max_length=200, default='', verbose_name='password for sending email',blank=True,)
    mail_srv      = models.CharField(max_length=200, default='', verbose_name='server for sending email',blank=True,)
    mail_port     = models.IntegerField(default=0, verbose_name='email server port')
    mail_tls      = models.BooleanField(default=True, verbose_name='use TLS',)

    def __str__(self):
        return self.url
    class Meta:
        verbose_name = "website"
        verbose_name_plural = "1.1 · URL & Settings"

#———————————————————————————————————————— page · uses template & prefix

from ckeditor.fields import RichTextField

class Page(models.Model): 
    visitable = models.BooleanField(default=True, verbose_name='published',)
    screen = models.ForeignKey(Screen, default=1, on_delete=models.PROTECT, verbose_name='screen size',)
    language = models.ForeignKey(Language, default=3, on_delete=models.PROTECT, )

    # meta
    notes = models.TextField(max_length=2000, default='', blank=True)
    from datetime import datetime
    pub_date    = models.DateTimeField(default=datetime.now, blank=True, verbose_name='publication date',)
    url         = models.CharField(max_length=200, default='', verbose_name='address')
    category    = models.CharField(max_length=200, default='Main', verbose_name='category', blank=True,)

    # used in page construction
    title  = models.CharField(max_length=200, default='', blank=True)

    # accessibility
    accessibility_name = models.CharField(max_length=200, default='', blank=True, verbose_name='page name')
    accessibility_text = RichTextField(verbose_name='accessibility content', blank=True)

    suppress_modules = models.BooleanField(default=False, verbose_name='suppress default modules',)

    module = models.ManyToManyField(Module, through='PageModule')
    script = models.ManyToManyField(Script, through='PageScript')

    override_dims = models.BooleanField(default=False, verbose_name='override default dimensions',)
    width = models.PositiveSmallIntegerField(default=0, verbose_name='Illustrator width')
    visible = models.PositiveSmallIntegerField(default=0, verbose_name='visible width')
    offsetx = models.PositiveSmallIntegerField(default=0, verbose_name='offset x')
    offsety = models.PositiveSmallIntegerField(default=0, verbose_name='offset y')

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.url
    class Meta:
        ordering = ['-visitable', 'url', 'language', 'screen', '-pub_date', ]
        verbose_name_plural = "2.2 · Pages"
    eache_reset   = models.BooleanField(default=False, verbose_name='delete cache (or visit example.com/c)',)
#   def __str__(self):
#       return '{} - {} ({})'.format(self.pk, self.name, self.pcode)

#———————————————————————————————————————— page models

# rename to pageModule
class PageModule(models.Model):
    page   = models.ForeignKey(Page,   on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    zindex = models.IntegerField(default=0, verbose_name='z index')
    active = models.BooleanField(default=True, verbose_name='active',)
    def __str__(self):
        return self.module.name
    class Meta:
        verbose_name = "link to module"
        verbose_name_plural = "links to modules"
        ordering = ["zindex"]

# script like module, available sitewide
class PageScript(models.Model):
    page   = models.ForeignKey(Page,   on_delete=models.CASCADE)
    script = models.ForeignKey(Script, on_delete=models.CASCADE)
    order  = models.IntegerField(default=0, verbose_name='load order')
    active = models.BooleanField(default=True, verbose_name='active',)
    def __str__(self):
        return self.script.name
    class Meta:
        verbose_name = "link to script"
        verbose_name_plural = "links to script"
        ordering = ["order"]

class Illustrator(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    filename = models.CharField(max_length=200, default='')
    zindex = models.IntegerField(default=0, verbose_name='z index')
    active = models.BooleanField(default=True, verbose_name='active',)
    def __str__(self):
        return self.filename
    class Meta:
        verbose_name = "Illustrator file"
        verbose_name_plural = "Illustrator files"
        ordering = ["zindex"]

# scripts added at bottom of page
# should be renamed to AdditonalScrpts
class AdditionalScript(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, default='', choices=Choices(*script_types), verbose_name='type')
    name = models.CharField(max_length=200, default='')
    content = models.TextField(max_length=50000, default='', verbose_name='content',)
    order = models.IntegerField(default=0, verbose_name='load order')
    active = models.BooleanField(default=True, verbose_name='active',)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "additional script"
        verbose_name_plural = "additional scripts"
        ordering = ["order"]


#———————————————————————————————————————— fin
