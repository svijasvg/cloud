
#:::::::::::::::::::::::::::::::::::::::: models.py

#———————————————————————————————————————— import

from django.contrib import admin
from urllib.parse import quote

admin.site.site_header = 'Main Settings List'   # was H1 in black bar, now title attribute of logo image
admin.site.site_title  = 'Svija Cloud'          # end of each admin page’s <title> (a string). By default, this is “Django site admin”.
admin.site.index_title = 'Svija Cloud Settings' # top of the admin index page (a string). By default, this is “Site administration”.

#———————————————————————————————————————— Control · no dependencies

from .models import Control
class ControlAdmin(admin.ModelAdmin):

  # display on parent page
  list_display = ('limit', 'used', 'cached',)
  save_on_top = True
  save_as = True

  fieldsets = [ 
    ('site settings',   {'fields': [('limit', 'cached'), ('used', 'password',),],}),
  ]   

admin.site.register(Control, ControlAdmin)

#———————————————————————————————————————— Redirect · no dependencies

descRedirect = "Start with <b>/</b> for internal links, <b>https://</b> for other sites · <a href=https://tech.svija.love/programs/cloud/redirects target=_blank>documentation↑</a>"

from .models import Redirect
class RedirectAdmin(admin.ModelAdmin):

  # display on parent page
  list_display = ('from_url', 'to_url', 'enabled', )
  save_on_top = True
  save_as = True

  fieldsets = [ 
    ('redirect settings',  {'fields': ['from_url', 'to_url','enabled',], 'description':descRedirect,}),
  ]   

admin.site.register(Redirect, RedirectAdmin)

#———————————————————————————————————————— Font · no dependencies

# https://stackoverflow.com/questions/15285740/make-django-admin-to-display-no-more-than-100-characters-in-list-results

descFonts    = 'Fonts added automatically the first time page is loaded · <a target="_blank" href="https://fonts.adobe.com/my_fonts#web_projects-section">Adobe Fonts↑</a> · <a target="_blank" href="https://fonts.google.com">Google Fonts↑</a> · <a href=https://tech.svija.love/programs/cloud/fonts target=_blank>documentation↑</a>'

from .models import Font
class FontAdmin(admin.ModelAdmin):

  def adobe_id(self, obj):
    return obj.adobe_pasted[53:60]

  # display on parent page
  list_display = ('svg_ref', 'family', 'weight', 'style', 'adobe_id', 'google', 'woff', 'enabled', 'category',)
  list_filter = ('category', 'google', 'enabled', )
  save_on_top = True
  save_as = True

  fieldsets = [ 
    ('font information',  {'fields': [('enabled', 'google',), ('svg_ref', 'category',), ('family', 'woff',), ('weight', 'style',), ('adobe_pasted', 'adobe_url',), 'adobe_sheet', ], 'description':descFonts,}),

  ]   

admin.site.register(Font, FontAdmin)

#———————————————————————————————————————— Section · no dependencies

descSection  = "Website sections · see also <a href='/cloud/svija/screen/'>screen sizes</a> · <a href=https://tech.svija.love/programs/cloud/sections target=_blank>documentation↑</a>"

from .models import Section
class SectionAdmin(admin.ModelAdmin):

  # display on parent page
  list_display = ('code', 'name', 'default_page', 'title', 'email', 'order',)
  save_on_top = True
  save_as = True

  fieldsets = [ 
    ('details', {'fields': [('code', 'default_page', ),('name','order',),],'description':descSection, }),
    ('title & iPhone icon', {'fields': ['title', 'touch',],}),
    ('email settings',   {'fields': ['email', 'bcc', 'subject','mail_frm',], 'classes': ['collapse']}),
    ('contact form fields', {'fields': ['form_name', 'form_business', 'form_email','form_message','form_send',], 'classes': ['collapse'],}),
    ('status message & alerts', {'fields': ['form_status', 'form_sending','form_rcvd','form_alert_rcvd', 'form_alert_fail',], 'classes': ['collapse'],}),
    ('source code message', {'fields': ['comment'], 'classes': ['collapse']}),
  ]   

admin.site.register(Section, SectionAdmin)

#———————————————————————————————————————— Screen · no dependencies

descScreens    = "Supported screen sizes · for maximum pixel width, 0=unlimited · see also <a href='/cloud/svija/section/'>sections</a> · <a href=https://tech.svija.love/programs/cloud/screens target=_blank>documentation↑</a>"

from .models import Screen
class ScreenAdmin(admin.ModelAdmin):

  # display on parent page
  list_display = ('code', 'name', 'width', 'pixels', 'order', )
  save_on_top = True
  save_as = True

  fieldsets = [ 
    ('details',{'fields': [('code', 'pixels',),('name',  'order'),],'description':descScreens,}),
    ('pixel dimensions',{'fields': [('width', 'offsetx',), ('visible', 'offsety',), ]}),
#     ('image quality',{'fields': ['img_multiply', 'img_quality', ]}),
  ]   

admin.site.register(Screen, ScreenAdmin)

#———————————————————————————————————————— Robots · no dependencies

descRobots = "Tell search engines whether or not to index this website · <a href='https://en.wikipedia.org/wiki/Robots_exclusion_standard'>wikipedia</a> · <a href=https://tech.svija.love/programs/cloud/robots target=_blank>documentation↑</a>"

from .models import Robots
class RobotsAdmin(admin.ModelAdmin):

  # display on parent page
  list_display = ('name', 'contents' )
  save_on_top = True
  save_as = True

  fieldsets = [ 
    ('name & file contents',{'fields': ['name', 'contents', ], 'description':descRobots, }),
  ]   
  verbose_name = "robots.txt"

  verbose_name_plural = "robots.txt"

admin.site.register(Robots, RobotsAdmin)

#———————————————————————————————————————— Script Set · no dependencies

descScript0 = "Script Sets can be included here or in <a href=\"/cloud/svija/page/\">page settings</a> · <a href=https://tech.svija.love/programs/cloud/script-sets target=_blank>documentation↑</a>"
descScript1 = "Link to instructions at <a href=\"https://tech.svija.love\">tech.svija.love</a> and usage notes"

from .models import ScriptScripts
class ScriptScriptsInline(admin.TabularInline):
  model = ScriptScripts
  extra = 0 
  fields = ('enabled', 'name', 'type', 'order', 'content',)
  verbose_name = "script"
  verbose_name_plural = "scripts"

from .models import Script
class ScriptAdmin(admin.ModelAdmin):

  # display on parent script
  list_display = ('name', 'category', 'enabled','always',)
  list_filter = ('category', )
  save_on_top = True
  save_as = True

  fieldsets = [ 
     ('name & filename', {'fields': [('name', 'enabled',),('category', 'always',), ], 'description':descScript0, }),
     ('instructions'   , {'fields': [('url', 'instructions'),], 'classes': ['collapse'],'description':descScript1, }),
  ]   

  inlines = [ScriptScriptsInline]

admin.site.register(Script, ScriptAdmin)

#———————————————————————————————————————— Module · no dependencies

descModules = "Modules can be included here or in <b><a href='/cloud/svija/page/'>Page Settings</a></b> · <a href=https://tech.svija.love/programs/cloud/modules target=_blank>documentation↑</a>"
descDefaultY = "Link to instructions at <a href=\"https://tech.svija.love\">tech.svija.love</a> and usage notes"
positdesc = 'Superimposed on Illustrator page · negative = up ↖ left · positive = down ↘ right'

#———————————————————————————————————————— Module inline

from .models import ModuleScript
class ModuleScriptInline(admin.TabularInline):
  model = ModuleScript
  extra = 0 
  fields = ('enabled', 'name', 'type', 'order', 'content',)
  verbose_name = "script"
  verbose_name_plural = "scripts"
  classes = ['collapse', 'ifempty',]


from .models import Module
class ModuleAdmin(admin.ModelAdmin):

  class Media:
    js = ( 'admin/js/ifempty.js', )

  # display on parent module
  list_display = ('name', 'enabled', 'always', 'section', 'screen', 'filename', 'zindex', 'tag',)
  list_filter = ('section', 'screen', 'always', 'enabled', 'tag', )
  save_on_top = True
  save_as = True

  fieldsets = [ 
     ('name & filename', {'fields': [('name', 'enabled','always'),('tag', 'screen'), ('css_id', 'section',), ('filename','zindex', ),], 'description':descModules, }),
     ('instructions'   , {'fields': [('url', 'instructions'),], 'classes': ['collapse'],'description':descDefaultY, }),
     ('placement'    , {'fields': [('offsetx', 'position', ), ( 'offsety', 'corner', ),],'description': positdesc,}),
  ]   

  inlines = [ModuleScriptInline]

admin.site.register(Module, ModuleAdmin)

#———————————————————————————————————————— Settings · depends on robots

descSettings = "To request a different website address, please visit <a href='https://tech.svija.love/url' target='_blank'>tech.svija.love/url</a> · <a href=https://tech.svija.love/programs/cloud/settings target=_blank>documentation↑</a>"

from .models import Settings
class SettingsAdmin(admin.ModelAdmin):

  # display on parent page
  list_display = ('url', 'enabled', 'section', 'robots',)
  save_on_top = True
  save_as = True

  fieldsets = [ 
    ('website settings',   {'fields': [('url', 'enabled', 'p3_color',), ('analytics_id','tracking_on', ), ('section',), 'robots',],'description': descSettings,}),
    ('mail settings', {'fields': ['mail_id', 'mail_pass', 'mail_srv','mail_port','mail_tls',], 'classes': ['collapse']}),
#     ('backup preferences', {'fields': ['backup_interval', 'backup_next', ], 'classes': ['collapse']}),
  ]   

admin.site.register(Settings, SettingsAdmin)

#———————————————————————————————————————— Page

descPages  = "Settings specific to this page · see also <a href='/cloud/svija/module/'>modules</a> · <a href=https://tech.svija.love/programs/cloud/pages target=_blank>documentation↑</a>"
descPixels = "Values are in pixels · Check \"Override default dimensions\" to activate"

#———————————————————————————————————————— Page inlines

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
  verbose_name = "script set"
  verbose_name_plural = "script sets"
  classes = ['collapse', 'ifempty',]

class IllustratorInlinePage(admin.TabularInline):
  model = Illustrator
  extra = 0 
  #fields = ('zindex', 'filename',)
  fields = ('enabled','filename','zindex',)
  verbose_name_plural = 'Illustrator files'

class AdditionalScriptInline(admin.TabularInline):
  model = AdditionalScript
  extra = 0 
  fields = ('enabled', 'name', 'type', 'order', 'content',)
  verbose_name = "script"
  verbose_name_plural = "additional scripts"
#   classes = ['collapse']



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
    ('setup',      {'fields': [
                     'published',
                     ('url', 'screen'),
                     ('title', 'section'),
                    ],'description':descPages, }),
    ('more settings',  {'fields': [
                 ('category','incl_modules','incl_scripts',),
                 ('visible', 'offsetx', 'default_dims',),
                 ('width', 'offsety',),
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

