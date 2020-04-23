#———————————————————————————————————————— comments

# on_delete
#https://stackoverflow.com/questions/38388423/what-does-on-delete-do-on-django-models

#———————————————————————————————————————— svg_page.models

from django.db import models
import datetime
from django.utils import timezone

# pip install django-model-utils
from model_utils import Choices

#———————————————————————————————————————— redirects · no dependencies

class Forwards(models.Model): 
    active = models.BooleanField(default=True, verbose_name='active',)
    from_url = models.CharField(max_length=200, default='', verbose_name='from URL')
    to_prefix = models.CharField(max_length=5, default='', verbose_name='to prefix, http or https')
    to_page = models.CharField(max_length=200, default='', verbose_name='to page or domain')

    def __str__(self):
        return self.from_url
    class Meta:
        verbose_name = "Redirects"
        verbose_name_plural = "4.2 · Redirects"

#———————————————————————————————————————— fonts · no dependencies

class Font(models.Model): 
    css    = models.CharField(max_length=100, default='', verbose_name='CSS reference')
    family = models.CharField(max_length=100, default='', verbose_name='family', blank=True)
    style  = models.CharField(max_length=100, default='', verbose_name='weightStyle', blank=True)
    source = models.CharField(max_length=100, default='SOURCE NEEDED', verbose_name='source', blank=True)
    google = models.BooleanField(default=True, verbose_name='Google font',)
    active = models.BooleanField(default=True, verbose_name='include',)

    def __str__(self):
        return self.css
    class Meta:
        verbose_name = "Font"
        verbose_name_plural = "3.1 · Fonts"

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
    category = models.CharField(max_length=100, default='', verbose_name='category', blank=True,)
    author = models.CharField(max_length=100, default='', verbose_name='author', blank=True,)
    contents = RichTextField()
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "notes"
        verbose_name_plural = "4.4 · My Notes"

#———————————————————————————————————————— language · no dependencies

class Language(models.Model):
    name = models.CharField(max_length=100, default='')
    code = models.CharField(max_length=2, default='', blank=True, verbose_name='two-letter code',)
    flag = models.CharField(max_length=10, default='', blank=True, verbose_name='flag emoji',)
    display_order = models.PositiveSmallIntegerField(default=0, verbose_name='display order')

    title = models.CharField(max_length=100, default='', verbose_name='second part of page title',)
    touch = models.CharField(max_length=100, default='', blank=True, verbose_name='iPhone icon name',)

    bcc = models.CharField(max_length=200, default='', verbose_name='bcc: field for contact form',blank=True,)
    default = models.CharField(max_length=200, default='', verbose_name='sender if email fails verifcation',blank=True,)
    no_email = models.CharField(max_length=200, default='', verbose_name='sender if only phone number is given',blank=True,)
    subject = models.CharField(max_length=200, default='', verbose_name='email subject',blank=True,)
    mail_frm = models.CharField(max_length=200, default='', verbose_name='sending address in email body',blank=True,)

    email           = models.CharField(max_length=100, default='', blank=True, verbose_name='destination address',)
    form_name       = models.CharField(max_length=100, default='', blank=True, verbose_name='name label',)
    form_email      = models.CharField(max_length=100, default='', blank=True, verbose_name='email label',)
    form_send       = models.CharField(max_length=100, default='', blank=True, verbose_name='send button label',)
    form_status     = models.CharField(max_length=100, default='', blank=True, verbose_name='default message value',)

    form_sending    = models.CharField(max_length=100, default='', blank=True, verbose_name='message while sending',)
    form_rcvd       = models.CharField(max_length=100, default='', blank=True, verbose_name='message after sent',)
    form_alert_rcvd = models.CharField(max_length=100, default='', blank=True, verbose_name='message sent alert',)
    form_alert_fail = models.CharField(max_length=100, default='', blank=True, verbose_name='message failed alert',)

    comment       = models.TextField(max_length=5000, default='Site built entirely in SVG with Svija – visit svija.com for more information!', verbose_name='source code message', )

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['display_order']
        verbose_name_plural = "1.2 · Languages"

#———————————————————————————————————————— responsive · no dependencies

class Responsive(models.Model):
    name = models.CharField(max_length=200, default='')
    display_order = models.PositiveSmallIntegerField(default=0, verbose_name='display order')

    source_dir = models.CharField(max_length=200, default='', blank=True, verbose_name='source directory',)
    meta_tag = models.CharField(max_length=200, default='', blank=True)
    description = models.CharField(max_length=200, default='', blank=True)
    canonical = models.BooleanField(default=False, verbose_name='canonical page for search engines',)

    width   = models.PositiveSmallIntegerField(default=0, verbose_name='pixel width of AI document',blank=True,)
    visible = models.PositiveSmallIntegerField(default=0, verbose_name='visible width in pixels')
    offsetx = models.PositiveSmallIntegerField(default=0, verbose_name='offset x in pixels')
    offsety = models.PositiveSmallIntegerField(default=0, verbose_name='offset y in pixels')

    img_multiply = models.DecimalField(default=2.4, max_digits=2, decimal_places=1, verbose_name='resolution multiple')
    img_quality  = models.PositiveSmallIntegerField(default=0, verbose_name='JPG quality (0-100)')

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['display_order']
        verbose_name_plural = "1.3 · Responsive Options"

#———————————————————————————————————————— robots · no dependencies

class Robots(models.Model):
    name = models.CharField(max_length=200, default='')
    contents = models.TextField(max_length=5000, default='', verbose_name='file contents',blank=True,)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Robots.txt"
        verbose_name_plural = "4.1· Robots.txt"

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
        ordering = ['active', 'display_order']
        verbose_name_plural = "4.3 · Templates"

#———————————————————————————————————————— library scripts · no dependencies

library_scripts=('head JS', 'body JS', 'HTML', 'form', 'CSS',)

class LibraryScript(models.Model):

    name = models.CharField(max_length=200, default='')
    type = models.CharField(max_length=255, default='', choices=Choices(*library_scripts), verbose_name='type')
    sort1 = models.CharField(max_length=100, default='', verbose_name='main category', blank=True,)
    sort2 = models.CharField(max_length=100, default='', verbose_name='sub category', blank=True,)
    content = models.TextField(max_length=50000, default='', verbose_name='content',)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
    class Meta:
        ordering = ["type", "name", "sort1", "sort2"]
        verbose_name = "Optional Scripts"
        verbose_name_plural = "3.3 · Optional Scripts"

#———————————————————————————————————————— module · no dependencies

class Module(models.Model):

    name = models.CharField(max_length=200, default='')
    filename = models.CharField(max_length=200, default='', blank=True, verbose_name='SVG file (optional)',)
    cache_reset   = models.BooleanField(default=False, verbose_name='clear cache on next visit',)
    display_order = models.PositiveSmallIntegerField(default=0, verbose_name='display order')

    active = models.BooleanField(default=True, verbose_name='active',)
    sort1 = models.CharField(max_length=100, default='', verbose_name='main category', blank=True,)
    sort2 = models.CharField(max_length=100, default='', verbose_name='sub category', blank=True,)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['active', 'display_order', 'name', 'sort1', 'sort2',]
        verbose_name_plural = "2.2 · Modules"

module_scripts=('head JS', 'body JS', 'CSS',)

class ModuleScripts(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, default='', choices=Choices(*module_scripts), verbose_name='type')
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

#———————————————————————————————————————— shared scripts · dependent on responsive

class Shared(models.Model):
    name = models.CharField(max_length=200, default='', verbose_name='Scripts Name')
    responsive = models.ForeignKey(Responsive, default=0, on_delete=models.PROTECT, )
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Sitewide Scripts"
        verbose_name_plural = "3.2 · Sitewide Scripts"

shared_scripts=('CSS', 'head JS', 'body JS',)

class SharedScripts(models.Model):
    scripts = models.ForeignKey(Shared, on_delete=models.PROTECT)
    type = models.CharField(max_length=255, default='', choices=Choices(*shared_scripts), verbose_name='type')
    name = models.CharField(max_length=200, default='')
    content = models.TextField(max_length=50000, default='', verbose_name='content',)
    order = models.IntegerField(default=0, verbose_name='load order')
    active = models.BooleanField(default=True, verbose_name='active',)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "included script"
        ordering = ["order"]

#———————————————————————————————————————— prefix · uses responsive & language

class Prefix(models.Model):
    display_order = models.PositiveSmallIntegerField(default=0, verbose_name='display order')
    path = models.CharField(max_length=2, default='')
    default = models.CharField(max_length=20, default='', verbose_name='default page')
    responsive = models.ForeignKey(Responsive, default=0, on_delete=models.PROTECT, )
    language = models.ForeignKey(Language, default=0, on_delete=models.PROTECT, )
    module = models.ManyToManyField(Module, through='PrefixModules')
    def __str__(self):
        return self.path
    class Meta:
        verbose_name_plural = "1.4 · Prefix Codes"
        ordering = ['display_order']

class PrefixModules(models.Model):
    module = models.ForeignKey(Module, on_delete=models.PROTECT)
    prefix = models.ForeignKey(Prefix, on_delete=models.PROTECT)
    zindex = models.IntegerField(default=0, verbose_name='z index')
    active = models.BooleanField(default=True, verbose_name='active',)
    def __str__(self):
        return self.module.name
    class Meta:
        verbose_name = "module"
        verbose_name_plural = "modules"
        ordering = ["zindex"]

#———————————————————————————————————————— site settings · uses prefix & robots

backup_intervals = ('none', '6 hrs', 'daily', 'weekly', 'monthly', 'quarterly',)

class Settings(models.Model):

    prefix = models.ForeignKey(Prefix, default=0, on_delete=models.PROTECT, verbose_name='default prefix')
    robots = models.ForeignKey(Robots, default=0, on_delete=models.PROTECT, verbose_name='robots.txt')
    analytics_id  = models.CharField(max_length=200, default='', verbose_name='analytics ID',blank=True,)
    url           = models.CharField(max_length=200, default='', verbose_name='site URL',)
    cached        = models.BooleanField(default=False, verbose_name='admins see cached content',)
    tracking_on   = models.BooleanField(default=False, verbose_name='cookies allowed by default',)

    cache_reset   = models.BooleanField(default=False, verbose_name='clear cache on next visit DEPRECATED',)

    secure        = models.BooleanField(default=True, verbose_name='HTTPS',)
    maps_api_key  = models.CharField(max_length=200, default='', verbose_name='Google Maps API key',blank=True,)
    active        = models.BooleanField(default=False, verbose_name='active',)

    # backup settings
    backup_interval = models.CharField(max_length=255, default='', choices=Choices(*backup_intervals), verbose_name='backup interval')
    backup_next     = models.BooleanField(default=False, verbose_name='back up on next visit',)

    # email settings
    mail_id          = models.CharField(max_length=200, default='', verbose_name='username for sending email',blank=True,)
    mail_pass  = models.CharField(max_length=200, default='', verbose_name='password for sending email',blank=True,)
    mail_srv  = models.CharField(max_length=200, default='', verbose_name='server for sending email',blank=True,)
    mail_port = models.IntegerField(default=0, verbose_name='email server port')
    mail_tls = models.BooleanField(default=True, verbose_name='use TLS',)

    from datetime import datetime
    pub_date    = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return self.url
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "1.1 · Site Settings"

#———————————————————————————————————————— page · uses shared, template & prefix

class Page(models.Model): 
    display_order = models.PositiveSmallIntegerField(default=0, verbose_name='display order')
    visitable = models.BooleanField(default=True, verbose_name='visitable',)
    shared = models.ForeignKey(Shared, default=0, on_delete=models.PROTECT, )
    template = models.ForeignKey(Template, default=0, on_delete=models.PROTECT, )
    library_script = models.ManyToManyField(LibraryScript, blank=True)
    prefix = models.ForeignKey(Prefix, default=0, on_delete=models.PROTECT, )
    cache_reset   = models.BooleanField(default=False, verbose_name='clear cache on next visit',)

    # unused or meta
    notes = models.TextField(max_length=2000, default='', blank=True)
    from datetime import datetime
    pub_date    = models.DateTimeField(default=datetime.now, blank=True)
    url    = models.CharField(max_length=200, default='', verbose_name='slug (follows prefix)')

    # used in page construction
    title  = models.CharField(max_length=200, default='', blank=True)

    # search snippet
    snippet_name = models.CharField(max_length=200, default='', blank=True, verbose_name='page name')
    snippet_text = models.TextField(max_length=50000, default='', blank=True, verbose_name='snippet content')

    suppress_modules = models.BooleanField(default=False, verbose_name='suppress default modules',)
    module = models.ManyToManyField(Module, through='PageModules')

    override_dims = models.BooleanField(default=False, verbose_name='override dimensions',)
    width = models.PositiveSmallIntegerField(default=0, verbose_name='page width in pixels')
    visible = models.PositiveSmallIntegerField(default=0, verbose_name='visible width in pixels')
    offsetx = models.PositiveSmallIntegerField(default=0, verbose_name='offset x in pixels')
    offsety = models.PositiveSmallIntegerField(default=0, verbose_name='offset y in pixels')

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.url
    class Meta:
        ordering = ['visitable', 'display_order', 'prefix', 'url', '-pub_date', ]
        verbose_name_plural = "2.1 · Pages"

page_scripts=('head JS', 'body JS', 'CSS', 'HTML' , 'form',)

class PageScripts(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, default='', choices=Choices(*page_scripts), verbose_name='type')
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
        verbose_name = "SVG file"
        verbose_name_plural = "SVG files"
        ordering = ["zindex"]

class PageModules(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    zindex = models.IntegerField(default=0, verbose_name='z index')
    active = models.BooleanField(default=True, verbose_name='active',)
    def __str__(self):
        return self.module.name
    class Meta:
        verbose_name = "module"
        verbose_name_plural = "modules"
        ordering = ["zindex"]

#———————————————————————————————————————— fin
