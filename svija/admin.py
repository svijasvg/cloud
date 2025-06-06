
#:::::::::::::::::::::::::::::::::::::::: admin.py

#———————————————————————————————————————— import

from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from urllib.parse import quote

admin.site.site_header = 'Main Settings List'   # was H1 in black bar, now title attribute of logo image
admin.site.site_title  = 'Svija Cloud'          # end of each admin page’s <title> (a string). By default, this is “Django site admin”.
admin.site.index_title = 'Svija Cloud Settings' # top of the admin index page (a string). By default, this is “Site administration”.

#———————————————————————————————————————— reused translations

text = _('scripts')
text = _('always include')
text = _('artboard width')
text = _('contents')
text = _('display order')
text = _('enabled')
text = _('fonts')
text = _('illustrator file')
text = _('illustrator files')
text = _('included script')
text = _('included scripts')
text = _('instructions')
text = _('instructions link')
text = _('instructions notes')
text = _('link instructions') 
text = _('load order')
text = _('name')
text = _('screen size')
text = _('script')
text = _('script content')
text = _('script name')
text = _('script library')
text = _('script libraries')
text = _('script type')
text = _('scripts')
text = _('section')
text = _('settings')
text = _('title')
text = _('visible width')
text = _('x offset')
text = _('y offset')
text = _('z index')

#———————————————————————————————————————— control · no dependencies

from .models import Control
class ControlAdmin(admin.ModelAdmin):

  # prevent bulk deletion in list view except in debug mode
  # https://gaetangrond.me/posts/django/protecting-data-in-django-admin-preventing-accidental-deletions/
  def has_add_permission(self, request, obj=None):
    return settings.DEBUG

  def has_delete_permission(self, request, obj=None):
    return settings.DEBUG

  # display on parent page
  list_display = ('limit', 'used', 'cached',)
  save_on_top = True
  save_as = True

  fieldsets = [ 
    ('site settings',   {'fields': [('limit', 'cached'), ('used', 'password',),],}),
  ]   

admin.site.register(Control, ControlAdmin)

#———————————————————————————————————————— redirect · no dependencies

descRedirect = _("descRedirect")
#escRedirect = "Start with <b>/</b> for internal links, <b>https://</b> for other sites · <a href=https://tech.svija.love/programs/cloud/redirects target=_blank>documentation↑</a>"

from .models import Redirect
class RedirectAdmin(admin.ModelAdmin):

  # display on parent page
  list_display = ('from_url', 'to_url', 'enabled', )
  save_on_top = True
  save_as = True

  fieldsets = [ 
    (_('settings'),  {'fields': ['from_url', 'to_url','enabled',], 'description':descRedirect,}),
  ]   

admin.site.register(Redirect, RedirectAdmin)

#———————————————————————————————————————— font · no dependencies

# https://stackoverflow.com/questions/15285740/make-django-admin-to-display-no-more-than-100-characters-in-list-results

descFonts = _('descFonts')

from .models import Font
class FontAdmin(admin.ModelAdmin):

  # display on parent page · order is determined in model def
  list_display = ('svg_ref', 'enabled', 'family', 'weight', 'style', 'google', 'adobe', 'woff', 'category',)
  list_filter = ('category', 'google', 'enabled', )
  save_on_top = True
  save_as = True

  fieldsets = [ 
    (_('font settings'),  {'fields': [('enabled', 'google','adobe', ), ('svg_ref', 'family',), ('woff', 'weight',), ('adobe_url', 'style',),'category',], 'description':descFonts,}),
  ]   

admin.site.register(Font, FontAdmin)

#———————————————————————————————————————— section · no dependencies

descSection  = _('descSection')
#escSection  = "Website sections · see also <a href='/cloud/svija/screen/'>screen sizes</a> · <a href=https://tech.svija.love/programs/cloud/sections target=_blank>documentation↑</a>"

from .models import Section
class SectionAdmin(admin.ModelAdmin):

  # display on parent page
  list_display = ('code', 'name', 'enabled', 'default_page', 'title', 'email', 'order',)
  save_on_top = True
  save_as = True

  fieldsets = [ 
    (_('settings'), {'fields': [('code', 'enabled', 'language', ),('name', 'order',), 'default_page',],'description':descSection, }),
    (_('title iPhone icon'), {'fields': ['title', 'touch',],}),
    (_('section email settings'),   {'fields': ['email', 'bcc', 'subject','mail_frm',], 'classes': ['collapse']}),
    (_('contact form fields'), {'fields': ['form_name', 'form_business', 'form_email','form_message','form_send',], 'classes': ['collapse'],}),
    (_('status message alerts'), {'fields': ['form_status', 'form_sending','form_rcvd','form_alert_rcvd', 'form_alert_fail',], 'classes': ['collapse'],}),
    (_('section source message'), {'fields': ['comment'], 'classes': ['collapse']}),
  ]   

admin.site.register(Section, SectionAdmin)

#———————————————————————————————————————— screen · no dependencies

descScreens    = _('descScreens')
#escScreens    = "Supported screen sizes · for maximum pixel width, 0=unlimited · see also <a href='/cloud/svija/section/'>sections</a> · <a href=https://tech.svija.love/programs/cloud/screens target=_blank>documentation↑</a>"

from .models import Screen
class ScreenAdmin(admin.ModelAdmin):

  # display on parent page
  list_display = ('code', 'name', 'width', 'pixels', 'order', )
  save_on_top = True
  save_as = True

  fieldsets = [ 
    (_('screens details'),{'fields': [('code', 'pixels',),('name',  'order'),],'description':descScreens,}),
    (_('pixel dimensions'),{'fields': [('width', 'offsetx',), ('visible', 'offsety',), ]}),
#     ('image quality',{'fields': ['img_multiply', 'img_quality', ]}),
  ]   

admin.site.register(Screen, ScreenAdmin)

#———————————————————————————————————————— robots · no dependencies

descRobots = _('descRobots')
#escRobots = "Tell search engines whether or not to index this website · <a href='https://en.wikipedia.org/wiki/Robots_exclusion_standard'>wikipedia</a> · <a href=https://tech.svija.love/programs/cloud/robots target=_blank>documentation↑</a>"

from .models import Robots
class RobotsAdmin(admin.ModelAdmin):

  # display on parent page
  list_display = ('name', 'contents' )
  save_on_top = True
  save_as = True

  fieldsets = [ 
    (_('settings'),{'fields': ['name', 'contents', ], 'description':descRobots, }),
  ]   
  verbose_name = "robots.txt"

  verbose_name_plural = "robots.txt"

admin.site.register(Robots, RobotsAdmin)

#———————————————————————————————————————— script library · no dependencies

descScript = _('descScript')
descLinkInstr = _('link instructions')

from .models import ScriptScripts
class ScriptScriptsInline(admin.TabularInline):
  model = ScriptScripts
  extra = 0 
  fields = ('enabled', 'name', 'type', 'order', 'content',)
  verbose_name = _("script")
  verbose_name_plural = _("scripts")

from .models import Script
class ScriptAdmin(admin.ModelAdmin):

  # display on parent script
  list_display = ('name', 'category', 'enabled','always',)
  list_filter = ('category', )
  save_on_top = True
  save_as = True

  class Media:
    js = ( 'admin/js/ifempty.js', )

  fieldsets = [ 
     (_('settings'), {'fields': [('name', 'enabled',),('category', 'always',), ], 'description':descScript, }),
     (_('instructions') , {'fields': [('instructions', 'url', ),], 'classes': ['collapse', 'ifempty',],'description':descLinkInstr, }),
  ]   

  inlines = [ScriptScriptsInline]

admin.site.register(Script, ScriptAdmin)

#———————————————————————————————————————— module · no dependencies

descModules  = _('descModules') 
#escLinkInstr = _('link instructions') # ABOVE, IN SCRIPT SET
positdesc    = _('positdesc') 
#escModules = "Modules can be included here or in <b><a href='/cloud/svija/page/'>Page Settings</a></b> · <a href=https://tech.svija.love/programs/cloud/modules target=_blank>documentation↑</a>"
#escDefaultY = "Link to instructions at <a href=\"https://tech.svija.love\">tech.svija.love</a> and usage notes"
#ositdesc = 'Superimposed on Illustrator page · negative = up ↖ left · positive = down ↘ right'

#———————————————————————————————————————— Module inline

# my SO question & answer
# https://stackoverflow.com/questions/73108883/is-there-a-way-to-make-a-collapsed-inline-initially-visible-in-django-admin-if

from .models import ModuleScript
class ModuleScriptInline(admin.TabularInline):
  model = ModuleScript
  extra = 0 
  fields = ('enabled', 'name', 'type', 'order', 'content',)
  verbose_name = _("script")
  verbose_name_plural = _("scripts")

# my SO question & answer
# https://stackoverflow.com/questions/73108883/is-there-a-way-to-make-a-collapsed-inline-initially-visible-in-django-admin-if
  classes = ['collapse', 'ifempty',]


from .models import Module
class ModuleAdmin(admin.ModelAdmin):

  class Media:
    js = ( 'admin/js/ifempty.js', )

  # display on parent module
  list_display = ('name', 'enabled', 'always', 'section', 'screen', 'filename', 'zindex', 'tag_header',)
  list_filter = ('section', 'screen', 'always', 'enabled', 'tag', )
  save_on_top = True
  save_as = True

  @admin.display(description='tag')
  def tag_header(self,obj) :
     return obj.tag

# @admin.filter(description='tag')
# def tag_header(self,obj) :
#    return obj.tag

  fieldsets = [ 
     (_('settings'     ), {'fields': [('name', 'enabled','always'),('tag', 'screen'), ('css_id', 'section',), ('filename','zindex', ),], 'description':descModules, }),
     (_('instructions' ), {'fields': [('instructions', 'url'),], 'classes': ['collapse', 'ifempty', ],'description':descLinkInstr, }),
     (_('placement'    ), {'fields': [('offsetx', 'corner', ), ( 'offsety', 'position', ),],'description': positdesc,}),
  ]   

  inlines = [ModuleScriptInline]

admin.site.register(Module, ModuleAdmin)

#———————————————————————————————————————— settings · depends on robots

descSettings = _('descSettings')
descAdobeProject= _('descAdobeProject')
descColors= _('descColors')

from .models import Settings
class SettingsAdmin(admin.ModelAdmin):

  # prevent bulk deletion in list view except in debug mode
  # https://gaetangrond.me/posts/django/protecting-data-in-django-admin-preventing-accidental-deletions/
  def has_add_permission(self, request, obj=None):
    return settings.DEBUG

  def has_delete_permission(self, request, obj=None):
    return settings.DEBUG

  # display on parent page
  list_display = ('url', 'enabled', 'section', 'robots',)
  save_on_top = True
  save_as = True

  fieldsets = [ 
    (_('website settings'), {'fields': [('url', 'enabled', 'p3_color',), ('analytics_id', 'tracking_on', ), 'section', 'robots',],'description': descSettings,}),
    (_('adobe web project'), {'fields': ['adobe_project', 'adobe_sheet',],'description': descAdobeProject,}),
    (_('svija cloud colors'), {'fields': [('color_main', 'color_dark', 'color_accent',),],'description': descColors,}),
    (_('email sending'   ), {'fields': [('mail_id', 'mail_pass'), ('mail_srv','mail_port','mail_tls'),'notes',], 'classes': ['collapse']}),
#     ('backup preferences', {'fields': ['backup_interval', 'backup_next', ], 'classes': ['collapse']}),
  ]   

admin.site.register(Settings, SettingsAdmin)

#———————————————————————————————————————— page inlines

from .models import Page, Illustrator
from .models import PageScript
from .models import AdditionalScript

class ModuleInlinePage(admin.TabularInline):
  model = Page.module.through
  extra = 0 
  fields = ('enabled', 'module', 'zindex', )
  verbose_name = "module"
  verbose_name_plural = "modules"
  classes = ['collapse', 'ifempty',]

class ScriptInlinePage(admin.TabularInline):
  model = Page.script.through
  extra = 0 
  fields = ('enabled', 'script',)
  verbose_name = _("script library")
  verbose_name_plural = _("script libraries")
  classes = ['collapse', 'ifempty',]

class IllustratorInlinePage(admin.TabularInline):
  model = Illustrator
  extra = 0 
  #fields = ('zindex', 'filename',)
  fields = ('enabled','filename','zindex',)
  verbose_name_plural = _('illustrator files')

class AdditionalScriptInline(admin.TabularInline):
  model = AdditionalScript
  extra = 0 
  fields = ('enabled', 'name', 'type', 'order', 'content',)
  verbose_name = _("script")
  verbose_name_plural = _("scripts")
#   classes = ['collapse']

#———————————————————————————————————————— page

descPages  = _('descPages')
#descPixels = _('descPixels')

#escPages  = "Settings specific to this page · see also <a href='/cloud/svija/module/'>modules</a> · <a href=https://tech.svija.love/programs/cloud/pages target=_blank>documentation↑</a>"
#escPixels = "Values are in pixels · Check \"Override default dimensions\" to activate"

# https://stackoverflow.com/questions/16014719/adding-a-jquery-script-to-the-django-admin-interface

class PageAdmin(admin.ModelAdmin):

  class Media:
    js = ( 'admin/js/ifempty.js', )

  # display on parent page
  list_display = ('url', 'title', 'published', 'section', 'screen', 'illustrator_file', 'incl_modules', 'category',)
  list_filter = ('section', 'screen', 'published', 'category', )
  save_on_top = True
  save_as = True

# https://stackoverflow.com/questions/38827608/get-list-display-in-django-admin-to-display-the-many-end-of-a-many-to-one-rela

  def get_queryset(self, obj):
    qs = super(PageAdmin, self).get_queryset(obj)
    return qs.prefetch_related('illustrator_fk')

  def illustrator_file(self,obj):
    return obj.illustrator_fk.filter(enabled=True).first()

  fieldsets = [ 
    (_('page setup'),      {'fields': [
                     'published',
                     ('url', 'screen'),
                     ('title', 'section'),
                    ],'description':descPages, }),
    (_('more page settings'),  {'fields': [
                 ('category','incl_modules','incl_scripts',),
                 ('width', 'offsetx', 'default_dims',),
                 ('visible', 'offsety',),
                 'accessibility_name',
                 'accessibility_text',
                 'notes', 'pub_date',
               ], 'classes': ['collapse'],}),

#     ('page info',    {'fields': [], 'classes': ['collapse'],}),
#     ('new dimensions', {'fields': [ ], 'classes': ['collapse'], 'description':descPixels,}),
  ]   

  inlines = [IllustratorInlinePage, AdditionalScriptInline, ModuleInlinePage, ScriptInlinePage, ]

admin.site.register(Page, PageAdmin)


#:::::::::::::::::::::::::::::::::::::::: fin

