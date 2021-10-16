#———————————————————————————————————————— models.py

#———————————————————————————————————————— notes

# CHANGING MODEL NAMES IMPLIES CHANGING STATIC/ADMIN_EXTRA.CSS

# on_delete
#https://stackoverflow.com/questions/38388423/what-does-on-delete-do-on-django-models

#———————————————————————————————————————— imports

from django.db import models
import datetime
from django.utils import timezone

# pip install django-model-utils
from model_utils import Choices

#———————————————————————————————————————— types of scripts

script_types = ('CSS', 'head JS', 'body JS', 'HTML', 'form',)

#———————————————————————————————————————— redirects · no dependencies

class Forwards(models.Model): 
    active = models.BooleanField(default=True, verbose_name='active',)
    from_url = models.CharField(max_length=200, default='', verbose_name='old URL')
    to_prefix = models.CharField(max_length=5, default='', verbose_name='HTTP or HTTPS', blank=True)
    to_page = models.CharField(max_length=200, default='', verbose_name='new URL')

    def __str__(self):
        return self.from_url
    class Meta:
        verbose_name = "redirect"
        verbose_name_plural = "4.2 · Redirects"

#———————————————————————————————————————— fonts · no dependencies

class Font(models.Model): 
    css    = models.CharField(max_length=100, default='', verbose_name='SVG name')
    family = models.CharField(max_length=100, default='', verbose_name='family', blank=True)
    style  = models.CharField(max_length=100, default='', verbose_name='weightStyle', blank=True)
    source = models.CharField(max_length=100, default='SOURCE NEEDED', verbose_name='WOFF filename', blank=True)
    google = models.BooleanField(default=True, verbose_name='Google font',)
    active = models.BooleanField(default=True, verbose_name='include',)

    def __str__(self):
        return self.css
    class Meta:
        verbose_name = "font"
        verbose_name_plural = "2.3 · Fonts"
        ordering = ['-active', 'family', 'style']

#———————————————————————————————————————— help · no dependencies

from ckeditor.fields import RichTextField

class Help(models.Model):
    name = models.CharField(max_length=200, default='')
    cat1 = models.CharField(max_length=100, default='', verbose_name='main category', blank=True,)
    cat2 = models.CharField(max_length=100, default='', verbose_name='sub  category', blank=True,)
    link = models.CharField(max_length=100, default='', verbose_name='link', blank=True,)
    contents = RichTextField()
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "help article"
        verbose_name_plural = "4.5 · Help"

#———————————————————————————————————————— notes · no dependencies

from ckeditor.fields import RichTextField

class Notes(models.Model):
    name = models.CharField(max_length=200, default='')
    category = models.CharField(max_length=100, default='', verbose_name='sort category', blank=True,)
    author = models.CharField(max_length=100, default='', verbose_name='author', blank=True,)
    contents = RichTextField()
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "note"
        verbose_name_plural = "4.4 · My Notes"

#———————————————————————————————————————— language · no dependencies

class Language(models.Model):
    name = models.CharField(max_length=100, default='')
    code = models.CharField(max_length=2, default='', blank=True, verbose_name='two-letter code',)
    flag = models.CharField(max_length=10, default='', blank=True, verbose_name='flag emoji',)
    #efault = models.CharField(max_length=20, default='', verbose_name='default page')
    default  = models.CharField(max_length=200, default='', verbose_name='default page',blank=True,)
    display_order = models.PositiveSmallIntegerField(default=0, verbose_name='display order')

    title = models.CharField(max_length=100, default='', verbose_name='second part of page title',)
    touch = models.CharField(max_length=100, default='', blank=True, verbose_name='iPhone icon name',)

    email    = models.CharField(max_length=100, default='', blank=True, verbose_name='destination address',)
    subject  = models.CharField(max_length=200, default='', verbose_name='email subject',blank=True,)
    mail_frm = models.CharField(max_length=200, default='', verbose_name='return address label',blank=True,)

    # 3 deprecated fields
    bcc      = models.CharField(max_length=200, default='', verbose_name='bcc: address',blank=True,)
    no_email = models.CharField(max_length=200, default='', verbose_name='sender if only phone number is given',blank=True,)

    form_name       = models.CharField(max_length=100, default='', blank=True, verbose_name='name',)
    form_business   = models.CharField(max_length=100, default='', blank=True, verbose_name='business',)
    form_email      = models.CharField(max_length=100, default='', blank=True, verbose_name='email',)
    form_status     = models.CharField(max_length=100, default='', blank=True, verbose_name='message',)
    form_send       = models.CharField(max_length=100, default='', blank=True, verbose_name='send button',)

    form_sending    = models.CharField(max_length=100, default='', blank=True, verbose_name='while sending',)
    form_alert_fail = models.CharField(max_length=100, default='', blank=True, verbose_name='sending failed',)
    form_rcvd       = models.CharField(max_length=100, default='', blank=True, verbose_name='once sent',)
    form_alert_rcvd = models.CharField(max_length=100, default='', blank=True, verbose_name='once sent (alert)',)

    comment       = models.TextField(max_length=5000, default='Site built entirely in SVG with Svija – visit svija.com for more information!', verbose_name='source code message', )

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['display_order']
        verbose_name_plural = "1.2 · Languages"

#———————————————————————————————————————— screen size was responsive · no dependencies

class Responsive(models.Model):
    name = models.CharField(max_length=200, default='')
    code = models.CharField(max_length=2, default='', blank=True, verbose_name='two-letter code',)
    limit = models.PositiveSmallIntegerField(default=0, verbose_name='maximum pixel width',blank=True,)

    canonical = models.BooleanField(default=False, verbose_name='canonical page for search engines',)

    meta_tag = models.CharField(max_length=200, default='', blank=True)
    display_order = models.PositiveSmallIntegerField(default=0, verbose_name='display order')

    width   = models.PositiveSmallIntegerField(default=0, verbose_name='Illustrator pixel width',blank=True,)
    visible = models.PositiveSmallIntegerField(default=0, verbose_name='visible width in pixels')
    offsetx = models.PositiveSmallIntegerField(default=0, verbose_name='offset x in pixels')
    offsety = models.PositiveSmallIntegerField(default=0, verbose_name='offset y in pixels')

    # not currently implemented, so hidden
    img_multiply = models.DecimalField(default=2.4, max_digits=2, decimal_places=1, verbose_name='resolution multiple')
    img_quality  = models.PositiveSmallIntegerField(default=0, verbose_name='JPG quality (0-100)')

    # deprecated
    source_dir = models.CharField(max_length=200, default='', blank=True, verbose_name='folder in /sync',)
    description = models.CharField(max_length=200, default='', blank=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['display_order']
        verbose_name = "screen size"
        verbose_name_plural = "1.3 · Screen Sizes"

#———————————————————————————————————————— robots · no dependencies

class Robots(models.Model):
    name = models.CharField(max_length=200, default='')
    contents = models.TextField(max_length=5000, default='', verbose_name='file contents',blank=True,)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "robots.txt"
        verbose_name_plural = "4.3 · Robots.txt"

#———————————————————————————————————————— template · no dependencies

class Template(models.Model):
    name = models.CharField(max_length=200, default='')
    filename = models.CharField(max_length=200, default='', blank=True, verbose_name='filename',)
    description = models.CharField(max_length=200, default='', blank=True)
    active = models.BooleanField(default=True, verbose_name='active',)
    display_order = models.PositiveSmallIntegerField(default=0, verbose_name='display order')

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-active', 'display_order']
        verbose_name_plural = "4.3 · Templates"

#———————————————————————————————————————— optional scripts · no dependencies

#deprecated
class OptionalScript(models.Model):

    name = models.CharField(max_length=200, default='')
    active = models.BooleanField(default=True, verbose_name='active',)
    type = models.CharField(max_length=255, default='', choices=Choices(*script_types), verbose_name='type')
    sort1 = models.CharField(max_length=100, default='', verbose_name='sort category', blank=True,)
    content = models.TextField(max_length=50000, default='', verbose_name='content',)

    # deprecated
    sort2 = models.CharField(max_length=100, default='', verbose_name='sub category', blank=True,)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-active', 'type', 'name', 'sort1', 'sort2']
        verbose_name = "DEPRECATED was optional script"
        verbose_name_plural = "DEPRECATED · was Optional Scripts"

#———————————————————————————————————————— modules · no dependencies

positions = ('absolute', 'floating', 'none',)
corners = ('top left', 'top right', 'bottom left', 'bottom right',)

class Module(models.Model):

    name = models.CharField(max_length=200, default='')
    active = models.BooleanField(default=True, verbose_name='published',)
    optional = models.BooleanField(default=False, verbose_name='always include',)
    screen = models.ForeignKey(Responsive, default=1, on_delete=models.PROTECT, verbose_name='screen size',)
    language = models.ForeignKey(Language, default=3, on_delete=models.PROTECT, verbose_name='language')
    sort1 = models.CharField(max_length=100, default='', verbose_name='sort label (optional)', blank=True,)
    display_order = models.PositiveSmallIntegerField(default=0, verbose_name='Z-index')
    css_id = models.CharField(max_length=200, default='', verbose_name='object ID (optional)', blank=True,)
    filename = models.CharField(max_length=200, default='', blank=True, verbose_name='Illustrator file (optional)',)
    notes = RichTextField(default='', blank=True, verbose_name='Instructions')

    cache_reset   = models.BooleanField(default=False, verbose_name='delete cache (or visit example.com/c)',)

    position = models.CharField(max_length=255, default='absolute', choices=Choices(*positions), verbose_name='placement')
    corner = models.CharField(max_length=255, default='top left', choices=Choices(*corners), verbose_name='relative to')
    horz_offset = models.FloatField(default=0, verbose_name='horizontal offset (px)',)
    vert_offset = models.FloatField(default=0, verbose_name='vertical offset (px)',)

    # deprecated
    sort2 = models.CharField(max_length=100, default='', verbose_name='sub category', blank=True,)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-active', 'sort1', 'name', 'screen',]
        verbose_name_plural = "2.2 · Modules"

class ModuleScripts(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, default='', choices=Choices(*script_types), verbose_name='type')
    name = models.CharField(max_length=200, default='')
    content = models.TextField(max_length=50000, default='', verbose_name='content',)
    order = models.IntegerField(default=0, verbose_name='load order')
    active = models.BooleanField(default=True, verbose_name='active',)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "extra script"
        verbose_name_plural = "extra scripts"
        ordering = ["order"]

#———————————————————————————————————————— script · responsive

#lass Shared(models.Model):
class DefaultScripts(models.Model):
    name = models.CharField(max_length=200, default='', verbose_name='name')
    active = models.BooleanField(default=True, verbose_name='active',)

    # deprecated
    responsive = models.ForeignKey(Responsive, default=2, on_delete=models.PROTECT, verbose_name='screen size',)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "scripts"
        verbose_name_plural = "4.1 · Scripts"

class DefaultScriptTypes(models.Model):
    scripts = models.ForeignKey(DefaultScripts, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, default='', choices=Choices(*script_types), verbose_name='type')
    name = models.CharField(max_length=200, default='')
    content = models.TextField(max_length=50000, default='', verbose_name='content',)
    order = models.IntegerField(default=0, verbose_name='load order')
    active = models.BooleanField(default=True, verbose_name='active',)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "single script"
        verbose_name_plural = "single scripts"
        ordering = ["order"]

#———————————————————————————————————————— deprecated prefixes combination codes · screen size & language

class Prefix(models.Model):
    display_order = models.PositiveSmallIntegerField(default=0, verbose_name='display order')
    path = models.CharField(max_length=2, default='', verbose_name='code',)
    default = models.CharField(max_length=20, default='', verbose_name='default page')
    responsive = models.ForeignKey(Responsive, default=0, on_delete=models.PROTECT, verbose_name='screen size',)
    language = models.ForeignKey(Language, default=0, on_delete=models.PROTECT, )
    module = models.ManyToManyField(Module, through='PrefixModules')
    def __str__(self):
        return self.path
    class Meta:
        verbose_name = "combination"
        verbose_name_plural = "1.4 · Combination Codes"
        ordering = ['display_order']

class PrefixModules(models.Model):
    module = models.ForeignKey(Module, on_delete=models.PROTECT)
    prefix = models.ForeignKey(Prefix, on_delete=models.PROTECT)
    zindex = models.IntegerField(default=0, verbose_name='z index')
    active = models.BooleanField(default=True, verbose_name='active',)
    def __str__(self):
        return self.module.name
    class Meta:
        verbose_name = "The following module is required by a combination code"
        verbose_name_plural = "The following modules are required by a combination code"
        ordering = ["zindex"]

#———————————————————————————————————————— site settings · combination code & robots

class Settings(models.Model):

    active        = models.BooleanField(default=False, verbose_name='online',)
    robots        = models.ForeignKey(Robots, default=0, on_delete=models.PROTECT, verbose_name='robots.txt')
    url           = models.CharField(max_length=200, default='', verbose_name='site URL',)
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

    # deprecated
    prefix        = models.ForeignKey(Prefix, default=0, on_delete=models.PROTECT, verbose_name='combination code default')
    cached        = models.BooleanField(default=False, verbose_name='admins see cached content',)
    secure        = models.BooleanField(default=True, verbose_name='HTTPS',)

    def __str__(self):
        return self.url
    class Meta:
        verbose_name = "website"
        verbose_name_plural = "1.1 · URL & Settings"

#———————————————————————————————————————— page · uses template & prefix

from ckeditor.fields import RichTextField

class Page(models.Model): 
    visitable = models.BooleanField(default=True, verbose_name='published',)
    screen = models.ForeignKey(Responsive, default=1, on_delete=models.PROTECT, verbose_name='screen size',)
    language = models.ForeignKey(Language, default=3, on_delete=models.PROTECT, )
    template = models.ForeignKey(Template, default=0, on_delete=models.PROTECT, )
    cache_reset   = models.BooleanField(default=False, verbose_name='delete cache (or visit example.com/c)',)
    default_scripts = models.ManyToManyField(DefaultScripts, blank=True)

    # unused or meta
    notes = models.TextField(max_length=2000, default='', blank=True)
    from datetime import datetime
    pub_date    = models.DateTimeField(default=datetime.now, blank=True)
    url    = models.CharField(max_length=200, default='', verbose_name='address')

    # used in page construction
    title  = models.CharField(max_length=200, default='', blank=True)

    # accessibility
    accessibility_name = models.CharField(max_length=200, default='', blank=True, verbose_name='page name')
    accessibility_text = RichTextField(verbose_name='accessibility content', blank=True)

    suppress_modules = models.BooleanField(default=False, verbose_name='suppress default modules',)
    module = models.ManyToManyField(Module, through='PageModules')

    override_dims = models.BooleanField(default=False, verbose_name='override default dimensions',)
    width = models.PositiveSmallIntegerField(default=0, verbose_name='Illustrator width')
    visible = models.PositiveSmallIntegerField(default=0, verbose_name='visible width')
    offsetx = models.PositiveSmallIntegerField(default=0, verbose_name='offset x')
    offsety = models.PositiveSmallIntegerField(default=0, verbose_name='offset y')

    # deprecated
    optional_script = models.ManyToManyField(OptionalScript, blank=True)
    display_order = models.PositiveSmallIntegerField(default=0, verbose_name='display order')
    prefix = models.ForeignKey(Prefix, default=3, on_delete=models.PROTECT, verbose_name='combination code',)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.url
    class Meta:
        ordering = ['-visitable', 'url', 'language', 'screen', '-pub_date', ]
        verbose_name_plural = "2.1 · Pages"
#   def __str__(self):
#       return '{} - {} ({})'.format(self.pk, self.name, self.pcode)


class PageScripts(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, default='', choices=Choices(*script_types), verbose_name='type')
    name = models.CharField(max_length=200, default='')
    content = models.TextField(max_length=50000, default='', verbose_name='content',)
    order = models.IntegerField(default=0, verbose_name='load order')
    active = models.BooleanField(default=True, verbose_name='active',)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "script"
        ordering = ["order"]

class Svg(models.Model):
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

class PageModules(models.Model):
    module = models.ForeignKey(Module, on_delete=models.PROTECT)
    page   = models.ForeignKey(Page,   on_delete=models.PROTECT)
    zindex = models.IntegerField(default=0, verbose_name='z index')
    active = models.BooleanField(default=True, verbose_name='active',)
    def __str__(self):
        return self.module.name
    class Meta:
        verbose_name = "The following module is required by a page"
        verbose_name_plural = "The following modules are required by a page"
        ordering = ["zindex"]


#———————————————————————————————————————— fin
