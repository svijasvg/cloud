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

class Redirect(models.Model): 
    active = models.BooleanField(default=True, verbose_name='active',)
    from_url = models.CharField(max_length=200, default='', verbose_name='from URL')
    to_prefix = models.CharField(max_length=5, default='', verbose_name='to prefix, http or https')
    to_page = models.CharField(max_length=200, default='', verbose_name='to page or domain')

    def __str__(self):
        return self.from_url

#———————————————————————————————————————— fonts · no dependencies

class Font(models.Model): 
    name   = models.CharField(max_length=100, default='', verbose_name='CSS reference')
    family = models.CharField(max_length=100, default='', verbose_name='family', blank=True)
    style  = models.CharField(max_length=100, default='', verbose_name='weightStyle', blank=True)
    source = models.CharField(max_length=100, default='', verbose_name='filename', blank=True)
    google = models.BooleanField(default=True, verbose_name='Google font',)
    active = models.BooleanField(default=True, verbose_name='active',)

    def __str__(self):
        return self.name

#———————————————————————————————————————— notes · no dependencies

from ckeditor.fields import RichTextField

class Notes(models.Model):
    name = models.CharField(max_length=200, default='')
    sort1 = models.CharField(max_length=100, default='', verbose_name='main category', blank=True,)
    sort2 = models.CharField(max_length=100, default='', verbose_name='sub category', blank=True,)
#   contents = models.TextField(max_length=20000, default='', verbose_name='note', blank=True,)
    contents = RichTextField()
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "notes"
        verbose_name_plural = "notes"

#———————————————————————————————————————— language · no dependencies

class Language(models.Model):
    name = models.CharField(max_length=100, default='')
    title = models.CharField(max_length=100, default='', verbose_name='page title',)
    touch = models.CharField(max_length=100, default='', verbose_name='iPhone icon name',)
    email = models.CharField(max_length=100, default='', verbose_name='destination email',)
    code = models.CharField(max_length=2, default='', blank=True, verbose_name='two-letter code',)

    form_name       = models.CharField(max_length=100, default='', verbose_name='name field',)
    form_email      = models.CharField(max_length=100, default='', verbose_name='email field',)
    form_status     = models.CharField(max_length=100, default='', verbose_name='status message',)
    form_send       = models.CharField(max_length=100, default='', verbose_name='send button',)

    form_sending    = models.CharField(max_length=100, default='', verbose_name='message while sending',)
    form_rcvd       = models.CharField(max_length=100, default='', verbose_name='message once sent',)

    form_alert_rcvd = models.CharField(max_length=100, default='', verbose_name='alert message sent',)
    form_alert_fail = models.CharField(max_length=100, default='', verbose_name='alert send failed',)

    bcc = models.CharField(max_length=200, default='', verbose_name='bcc: field for contact form',blank=True,)
    default = models.CharField(max_length=200, default='', verbose_name='sender when email fails verifcation',blank=True,)
    no_email = models.CharField(max_length=200, default='', verbose_name='sender when only phone number is given',blank=True,)
    subject = models.CharField(max_length=200, default='', verbose_name='email subject',blank=True,)
    mail_frm = models.CharField(max_length=200, default='', verbose_name='sending address in body',blank=True,)
    comment       = models.TextField(max_length=5000, default='', verbose_name='source comments',blank=True,)

    def __str__(self):
        return self.name

#———————————————————————————————————————— responsive · no dependencies

class Responsive(models.Model):
    name = models.CharField(max_length=200, default='')
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
        verbose_name_plural = "Responsive"

#———————————————————————————————————————— robots · no dependencies

class Robots(models.Model):
    name = models.CharField(max_length=200, default='')
    contents = models.TextField(max_length=5000, default='', verbose_name='file contents',blank=True,)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Robots.txt"
        verbose_name_plural = "Robots.txt"

#———————————————————————————————————————— template · no dependencies

class Template(models.Model):
    name = models.CharField(max_length=200, default='')
    filename = models.CharField(max_length=200, default='', blank=True, verbose_name='subfolder & filename',)
    description = models.CharField(max_length=200, default='', blank=True)
    active = models.BooleanField(default=True, verbose_name='active',)
    default = models.BooleanField(default=False, verbose_name='default',)
    def __str__(self):
        return self.name

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

#———————————————————————————————————————— module · no dependencies

class Module(models.Model):

    name = models.CharField(max_length=200, default='')
    filename = models.CharField(max_length=200, default='', blank=True)

    active = models.BooleanField(default=True, verbose_name='active',)
    sort1 = models.CharField(max_length=100, default='', verbose_name='main category', blank=True,)
    sort2 = models.CharField(max_length=100, default='', verbose_name='sub category', blank=True,)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name', 'active', 'sort1', 'sort2',]

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
    responsive = models.ForeignKey(Responsive, default=0, on_delete=models.CASCADE, )
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Shared Scripts"
        verbose_name_plural = "Shared Scripts"

shared_scripts=('CSS', 'head JS', 'body JS',)

class SharedScripts(models.Model):
    scripts = models.ForeignKey(Shared, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, default='', choices=Choices(*shared_scripts), verbose_name='type')
    name = models.CharField(max_length=200, default='')
    content = models.TextField(max_length=50000, default='', verbose_name='content',)
    order = models.IntegerField(default=0, verbose_name='load order')
    active = models.BooleanField(default=True, verbose_name='active',)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "shared script"
        verbose_name_plural = "shared scripts"
        ordering = ["order"]

#———————————————————————————————————————— prefix · uses responsive & language

class Prefix(models.Model):
    path = models.CharField(max_length=2, default='')
    default = models.CharField(max_length=20, default='', verbose_name='default page')
    responsive = models.ForeignKey(Responsive, default=0, on_delete=models.CASCADE, )
    language = models.ForeignKey(Language, default=0, on_delete=models.CASCADE, )
    module = models.ManyToManyField(Module, through='PrefixModules')
    def __str__(self):
        return self.path
    class Meta:
        verbose_name_plural = "Prefixes"

class PrefixModules(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    prefix = models.ForeignKey(Prefix, on_delete=models.CASCADE)
    order = models.IntegerField(default=0, verbose_name='load order')
    active = models.BooleanField(default=True, verbose_name='active',)
    def __str__(self):
        return self.module.name
    class Meta:
        verbose_name = "module"
        verbose_name_plural = "modules"
        ordering = ["order"]

#———————————————————————————————————————— site settings · uses prefix & robots

backup_intervals = ('none', '6 hrs', 'daily', 'weekly', 'monthly', 'quarterly',)

class Settings(models.Model):

    prefix = models.ForeignKey(Prefix, default=0, on_delete=models.CASCADE, verbose_name='default prefix')
    robots = models.ForeignKey(Robots, default=0, on_delete=models.CASCADE, verbose_name='robots.txt')
    analytics_id  = models.CharField(max_length=200, default='', verbose_name='analytics ID',blank=True,)
    url           = models.CharField(max_length=200, default='', verbose_name='site URL',)
    cached        = models.BooleanField(default=False, verbose_name='admins see cached content',)
    cache_reset   = models.BooleanField(default=False, verbose_name='clear cache on next visit',)
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
        verbose_name_plural = "Site Settings"

#———————————————————————————————————————— page · uses shared, template & prefix

class Page(models.Model): 
    visitable = models.BooleanField(default=True, verbose_name='visitable',)
    shared = models.ForeignKey(Shared, default=0, on_delete=models.CASCADE, )
    template = models.ForeignKey(Template, default=0, on_delete=models.CASCADE, )
    library_script = models.ManyToManyField(LibraryScript, blank=True)
    prefix = models.ForeignKey(Prefix, default=0, on_delete=models.CASCADE, )

    # unused or meta
    notes = models.TextField(max_length=2000, default='', blank=True)
    from datetime import datetime
    pub_date    = models.DateTimeField(default=datetime.now, blank=True)
    url    = models.CharField(max_length=200, default='', verbose_name='slug (follows prefix)')

    # used in page construction
    title  = models.CharField(max_length=200, default='', blank=True)

    # accessibility/seo text
    access_name = models.CharField(max_length=200, default='', blank=True, verbose_name='accessibility link name')
    access_text = models.TextField(max_length=50000, default='', blank=True, verbose_name='accessibility content')

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
        ordering = ["-pub_date"]

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
    order = models.IntegerField(default=0, verbose_name='load order')
    active = models.BooleanField(default=True, verbose_name='active',)
    def __str__(self):
        return self.filename
    class Meta:
        verbose_name = "SVG file"
        verbose_name_plural = "SVG files"
        ordering = ["order"]

class PageModules(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    order = models.IntegerField(default=0, verbose_name='load order')
    active = models.BooleanField(default=True, verbose_name='active',)
    def __str__(self):
        return self.module.name
    class Meta:
        verbose_name = "module"
        verbose_name_plural = "modules"
        ordering = ["order"]

#———————————————————————————————————————— fin
